use async_trait::async_trait;
use reqwest::Client;
use serde_json::{json, Value};
use tracing::{info, warn, error};

use crate::domain::{
    User, Role, Permission, Token, TokenValidation, TokenIntrospection,
    CreateUserRequest, UpdateUserRequest, UserEntity,
    UserRepository, TokenRepository, RoleRepository, PermissionRepository,
};
use crate::shared::result::{AppResult, AppError};
use crate::shared::result::{unauthorized_error, not_found_error, validation_error};

#[derive(Clone)]
pub struct KeycloakClient {
    base_url: String,
    realm: String,
    client_id: String,
    client_secret: String,
    http_client: Client,
}

impl KeycloakClient {
    pub fn new(base_url: String, realm: String, client_id: String, client_secret: String) -> Self {
        Self {
            base_url,
            realm,
            client_id,
            client_secret,
            http_client: Client::new(),
        }
    }

    async fn get_admin_token(&self) -> AppResult<String> {
        let url = format!("{}/realms/{}/protocol/openid-connect/token", self.base_url, "master");
        
        let params = [
            ("client_id", &self.client_id),
            ("client_secret", &self.client_secret),
            ("grant_type", &"client_credentials".to_string()),
        ];

        info!("Requesting admin token from Keycloak");

        let response = self.http_client
            .post(&url)
            .form(&params)
            .send()
            .await
            .map_err(|e| {
                error!("Failed to get admin token: {}", e);
                AppError::InfrastructureError(format!("Failed to connect to Keycloak: {}", e))
            })?;

        if !response.status().is_success() {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_default();
            error!("Keycloak admin token request failed: {} - {}", status, error_text);
            return Err(AppError::InfrastructureError(format!("Keycloak admin auth failed: {}", status)));
        }

        let token_data: Value = response.json().await
            .map_err(|e| {
                error!("Failed to parse admin token response: {}", e);
                AppError::InfrastructureError("Failed to parse Keycloak response".to_string())
            })?;

        token_data["access_token"]
            .as_str()
            .map(|s| s.to_string())
            .ok_or_else(|| {
                error!("Admin token not found in response");
                AppError::InfrastructureError("Failed to extract admin token".to_string())
            })
    }

    fn build_admin_request(&self, admin_token: &str) -> reqwest::RequestBuilder {
        self.http_client
            .get("") // Will be overridden by specific method calls
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
    }

    fn map_keycloak_user_to_domain(&self, keycloak_user: &Value) -> AppResult<User> {
        Ok(User {
            id: keycloak_user["id"]
                .as_str()
                .ok_or_else(|| validation_error("Missing user ID"))?
                .to_string(),
            email: keycloak_user["email"]
                .as_str()
                .unwrap_or_default()
                .to_string(),
            username: keycloak_user["username"]
                .as_str()
                .ok_or_else(|| validation_error("Missing username"))?
                .to_string(),
            first_name: keycloak_user["firstName"]
                .as_str()
                .unwrap_or_default()
                .to_string(),
            last_name: keycloak_user["lastName"]
                .as_str()
                .unwrap_or_default()
                .to_string(),
            enabled: keycloak_user["enabled"].as_bool().unwrap_or(false),
            email_verified: keycloak_user["emailVerified"].as_bool().unwrap_or(false),
            created_at: None, // Keycloak doesn't provide this in user representation
            updated_at: None, // Keycloak doesn't provide this in user representation
        })
    }

    fn map_keycloak_role_to_domain(&self, keycloak_role: &Value) -> AppResult<Role> {
        Ok(Role {
            id: keycloak_role["id"]
                .as_str()
                .map(|s| s.to_string())
                .unwrap_or_default(),
            name: keycloak_role["name"]
                .as_str()
                .ok_or_else(|| validation_error("Missing role name"))?
                .to_string(),
            description: keycloak_role["description"].as_str().map(|s| s.to_string()),
            composite: keycloak_role["composite"].as_bool().unwrap_or(false),
            client_role: keycloak_role["clientRole"].as_bool().unwrap_or(false),
            container_id: keycloak_role["containerId"]
                .as_str()
                .map(|s| s.to_string())
                .unwrap_or_default(),
        })
    }
}

#[async_trait]
impl UserRepository for KeycloakClient {
    async fn find_by_id(&self, id: &str) -> AppResult<Option<User>> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/users/{}", self.base_url, self.realm, id);

        info!("Fetching user by ID: {}", id);

        let response = self.http_client
            .get(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .send()
            .await
            .map_err(|e| {
                error!("Failed to fetch user by ID {}: {}", id, e);
                AppError::InfrastructureError(format!("Failed to fetch user: {}", e))
            })?;

        if response.status().is_success() {
            let user_data: Value = response.json().await
                .map_err(|e| {
                    error!("Failed to parse user response: {}", e);
                    AppError::InfrastructureError("Failed to parse user data".to_string())
                })?;
            
            let user = self.map_keycloak_user_to_domain(&user_data)?;
            Ok(Some(user))
        } else if response.status() == 404 {
            Ok(None)
        } else {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_default();
            error!("Keycloak user fetch failed: {} - {}", status, error_text);
            Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
        }
    }

    async fn find_by_username(&self, username: &str) -> AppResult<Option<User>> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/users", self.base_url, self.realm);

        info!("Searching user by username: {}", username);

        let response = self.http_client
            .get(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .query(&[("username", username), ("exact", "true")])
            .send()
            .await
            .map_err(|e| {
                error!("Failed to search user by username {}: {}", username, e);
                AppError::InfrastructureError(format!("Failed to search user: {}", e))
            })?;

        if response.status().is_success() {
            let users: Vec<Value> = response.json().await
                .map_err(|e| {
                    error!("Failed to parse users response: {}", e);
                    AppError::InfrastructureError("Failed to parse users data".to_string())
                })?;

            if let Some(user_data) = users.first() {
                let user = self.map_keycloak_user_to_domain(user_data)?;
                Ok(Some(user))
            } else {
                Ok(None)
            }
        } else {
            let status = response.status();
            error!("Keycloak user search failed: {}", status);
            Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
        }
    }

    async fn find_by_email(&self, email: &str) -> AppResult<Option<User>> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/users", self.base_url, self.realm);

        info!("Searching user by email: {}", email);

        let response = self.http_client
            .get(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .query(&[("email", email), ("exact", "true")])
            .send()
            .await
            .map_err(|e| {
                error!("Failed to search user by email {}: {}", email, e);
                AppError::InfrastructureError(format!("Failed to search user: {}", e))
            })?;

        if response.status().is_success() {
            let users: Vec<Value> = response.json().await
                .map_err(|e| {
                    error!("Failed to parse users response: {}", e);
                    AppError::InfrastructureError("Failed to parse users data".to_string())
                })?;

            if let Some(user_data) = users.first() {
                let user = self.map_keycloak_user_to_domain(user_data)?;
                Ok(Some(user))
            } else {
                Ok(None)
            }
        } else {
            let status = response.status();
            error!("Keycloak user search failed: {}", status);
            Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
        }
    }

    async fn create_user(&self, user_request: &CreateUserRequest) -> AppResult<User> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/users", self.base_url, self.realm);

        info!("Creating new user: {}", user_request.username);

        let user_data = json!({
            "username": user_request.username,
            "email": user_request.email,
            "firstName": user_request.first_name,
            "lastName": user_request.last_name,
            "enabled": true,
            "emailVerified": false,
            "credentials": [{
                "type": "password",
                "value": user_request.password,
                "temporary": false
            }]
        });

        let response = self.http_client
            .post(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .json(&user_data)
            .send()
            .await
            .map_err(|e| {
                error!("Failed to create user {}: {}", user_request.username, e);
                AppError::InfrastructureError(format!("Failed to create user: {}", e))
            })?;

        if response.status() == 201 {
            // Keycloak doesn't return the created user, so we need to fetch it
            info!("User created successfully, fetching created user");
            self.find_by_username(&user_request.username).await?
                .ok_or_else(|| {
                    error!("User created but not found when fetching");
                    AppError::InfrastructureError("User created but not found".to_string())
                })
        } else {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_default();
            error!("Keycloak user creation failed: {} - {}", status, error_text);
            
            if status == 409 {
                Err(AppError::InfrastructureError("User already exists".to_string()))
            } else {
                Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
            }
        }
    }

    async fn update_user(&self, user: &User) -> AppResult<User> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/users/{}", self.base_url, self.realm, user.id);

        info!("Updating user: {}", user.id);

        let user_data = json!({
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "enabled": user.enabled,
            "emailVerified": user.email_verified,
        });

        let response = self.http_client
            .put(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .json(&user_data)
            .send()
            .await
            .map_err(|e| {
                error!("Failed to update user {}: {}", user.id, e);
                AppError::InfrastructureError(format!("Failed to update user: {}", e))
            })?;

        if response.status().is_success() {
            info!("User updated successfully: {}", user.id);
            Ok(user.clone())
        } else {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_default();
            error!("Keycloak user update failed: {} - {}", status, error_text);
            Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
        }
    }

    async fn delete_user(&self, id: &str) -> AppResult<()> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/users/{}", self.base_url, self.realm, id);

        info!("Deleting user: {}", id);

        let response = self.http_client
            .delete(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .send()
            .await
            .map_err(|e| {
                error!("Failed to delete user {}: {}", id, e);
                AppError::InfrastructureError(format!("Failed to delete user: {}", e))
            })?;

        if response.status().is_success() {
            info!("User deleted successfully: {}", id);
            Ok(())
        } else if response.status() == 404 {
            Err(not_found_error("User", id))
        } else {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_default();
            error!("Keycloak user deletion failed: {} - {}", status, error_text);
            Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
        }
    }

    async fn username_exists(&self, username: &str) -> AppResult<bool> {
        Ok(self.find_by_username(username).await?.is_some())
    }

    async fn email_exists(&self, email: &str) -> AppResult<bool> {
        Ok(self.find_by_email(email).await?.is_some())
    }

    async fn validate_credentials(&self, username: &str, password: &str) -> AppResult<bool> {
        // Try to get a token with the credentials - if successful, credentials are valid
        let url = format!("{}/realms/{}/protocol/openid-connect/token", self.base_url, self.realm);
        
        let params = [
            ("client_id", self.client_id.as_str()),
            ("client_secret", self.client_secret.as_str()),
            ("grant_type", "password"),
            ("username", username),
            ("password", password),
        ];

        let response = self.http_client
            .post(&url)
            .form(&params)
            .send()
            .await
            .map_err(|e| {
                error!("Credential validation request failed for user {}: {}", username, e);
                AppError::InfrastructureError(format!("Validation request failed: {}", e))
            })?;

        Ok(response.status().is_success())
    }
}

#[async_trait]
impl TokenRepository for KeycloakClient {
    async fn generate_token(&self, username: &str, password: &str) -> AppResult<Token> {
        let url = format!("{}/realms/{}/protocol/openid-connect/token", self.base_url, self.realm);
        
        let params = [
            ("client_id", self.client_id.as_str()),
            ("client_secret", self.client_secret.as_str()),
            ("grant_type", "password"),
            ("username", username),
            ("password", password),
        ];

        info!("Generating token for user: {}", username);

        let response = self.http_client
            .post(&url)
            .form(&params)
            .send()
            .await
            .map_err(|e| {
                error!("Token generation failed for user {}: {}", username, e);
                AppError::InfrastructureError(format!("Token generation failed: {}", e))
            })?;

        if response.status().is_success() {
            let token_data: Value = response.json().await
                .map_err(|e| {
                    error!("Failed to parse token response: {}", e);
                    AppError::InfrastructureError("Failed to parse token data".to_string())
                })?;

            Ok(Token {
                access_token: token_data["access_token"]
                    .as_str()
                    .ok_or_else(|| validation_error("Missing access token"))?
                    .to_string(),
                refresh_token: token_data["refresh_token"]
                    .as_str()
                    .ok_or_else(|| validation_error("Missing refresh token"))?
                    .to_string(),
                expires_in: token_data["expires_in"]
                    .as_i64()
                    .unwrap_or(300),
                refresh_expires_in: token_data["refresh_expires_in"]
                    .as_i64()
                    .unwrap_or(1800),
                token_type: token_data["token_type"]
                    .as_str()
                    .unwrap_or("Bearer")
                    .to_string(),
                scope: token_data["scope"].as_str().map(|s| s.to_string()),
                session_state: token_data["session_state"].as_str().map(|s| s.to_string()),
            })
        } else {
            let status = response.status();
            error!("Token generation failed with status: {}", status);
            Err(unauthorized_error("Invalid credentials"))
        }
    }

    async fn refresh_token(&self, refresh_token: &str) -> AppResult<Token> {
        let url = format!("{}/realms/{}/protocol/openid-connect/token", self.base_url, self.realm);
        
        let params = [
            ("client_id", self.client_id.as_str()),
            ("client_secret", self.client_secret.as_str()),
            ("grant_type", "refresh_token"),
            ("refresh_token", refresh_token),
        ];

        info!("Refreshing token");

        let response = self.http_client
            .post(&url)
            .form(&params)
            .send()
            .await
            .map_err(|e| {
                error!("Token refresh failed: {}", e);
                AppError::InfrastructureError(format!("Token refresh failed: {}", e))
            })?;

        if response.status().is_success() {
            let token_data: Value = response.json().await
                .map_err(|e| {
                    error!("Failed to parse refresh token response: {}", e);
                    AppError::InfrastructureError("Failed to parse token data".to_string())
                })?;

            Ok(Token {
                access_token: token_data["access_token"]
                    .as_str()
                    .ok_or_else(|| validation_error("Missing access token"))?
                    .to_string(),
                refresh_token: token_data["refresh_token"]
                    .as_str()
                    .unwrap_or(refresh_token)
                    .to_string(),
                expires_in: token_data["expires_in"]
                    .as_i64()
                    .unwrap_or(300),
                refresh_expires_in: token_data["refresh_expires_in"]
                    .as_i64()
                    .unwrap_or(1800),
                token_type: token_data["token_type"]
                    .as_str()
                    .unwrap_or("Bearer")
                    .to_string(),
                scope: token_data["scope"].as_str().map(|s| s.to_string()),
                session_state: token_data["session_state"].as_str().map(|s| s.to_string()),
            })
        } else {
            let status = response.status();
            error!("Token refresh failed with status: {}", status);
            Err(unauthorized_error("Invalid refresh token"))
        }
    }

    async fn validate_token(&self, token: &str) -> AppResult<bool> {
        let url = format!("{}/realms/{}/protocol/openid-connect/token/introspect", self.base_url, self.realm);
        
        let params = [
            ("client_id", self.client_id.as_str()),
            ("client_secret", self.client_secret.as_str()),
            ("token", token),
        ];

        let response = self.http_client
            .post(&url)
            .form(&params)
            .send()
            .await
            .map_err(|e| {
                error!("Token validation failed: {}", e);
                AppError::InfrastructureError(format!("Token validation failed: {}", e))
            })?;

        if response.status().is_success() {
            let introspection: Value = response.json().await
                .map_err(|e| {
                    error!("Failed to parse token introspection: {}", e);
                    AppError::InfrastructureError("Failed to parse introspection data".to_string())
                })?;
            
            Ok(introspection["active"].as_bool().unwrap_or(false))
        } else {
            error!("Token introspection request failed");
            Ok(false)
        }
    }

    async fn introspect_token(&self, token: &str) -> AppResult<TokenIntrospection> {
        let url = format!("{}/realms/{}/protocol/openid-connect/token/introspect", self.base_url, self.realm);
        
        let params = [
            ("client_id", self.client_id.as_str()),
            ("client_secret", self.client_secret.as_str()),
            ("token", token),
        ];

        let response = self.http_client
            .post(&url)
            .form(&params)
            .send()
            .await
            .map_err(|e| {
                error!("Token introspection failed: {}", e);
                AppError::InfrastructureError(format!("Token introspection failed: {}", e))
            })?;

        if response.status().is_success() {
            let introspection_data: Value = response.json().await
                .map_err(|e| {
                    error!("Failed to parse token introspection data: {}", e);
                    AppError::InfrastructureError("Failed to parse introspection data".to_string())
                })?;

            Ok(TokenIntrospection::from_json_value(introspection_data))
        } else {
            error!("Token introspection request failed");
            Ok(TokenIntrospection::inactive())
        }
    }

    async fn logout(&self, refresh_token: &str) -> AppResult<()> {
        let url = format!("{}/realms/{}/protocol/openid-connect/logout", self.base_url, self.realm);
        
        let params = [
            ("client_id", self.client_id.as_str()),
            ("client_secret", self.client_secret.as_str()),
            ("refresh_token", refresh_token),
        ];

        info!("Logging out user");

        let response = self.http_client
            .post(&url)
            .form(&params)
            .send()
            .await
            .map_err(|e| {
                error!("Logout failed: {}", e);
                AppError::InfrastructureError(format!("Logout failed: {}", e))
            })?;

        if response.status().is_success() {
            info!("User logged out successfully");
            Ok(())
        } else {
            let status = response.status();
            error!("Logout failed with status: {}", status);
            Err(AppError::InfrastructureError("Logout failed".to_string()))
        }
    }

    async fn store_token(&self, _token: &Token, _user_id: &str) -> AppResult<()> {
        // Keycloak manages token storage, so this is a no-op
        Ok(())
    }

    async fn revoke_token(&self, _token: &str) -> AppResult<()> {
        // Keycloak manages token revocation through logout/introspection
        // For immediate revocation, we'd need to implement token revocation endpoint
        warn!("Token revocation not fully implemented for Keycloak");
        Ok(())
    }
}

#[async_trait]
impl RoleRepository for KeycloakClient {
    async fn find_by_id(&self, id: &str) -> AppResult<Option<Role>> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/roles-by-id/{}", self.base_url, self.realm, id);

        let response = self.http_client
            .get(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .send()
            .await
            .map_err(|e| {
                error!("Failed to fetch role by ID {}: {}", id, e);
                AppError::InfrastructureError(format!("Failed to fetch role: {}", e))
            })?;

        if response.status().is_success() {
            let role_data: Value = response.json().await
                .map_err(|e| {
                    error!("Failed to parse role response: {}", e);
                    AppError::InfrastructureError("Failed to parse role data".to_string())
                })?;
            
            let role = self.map_keycloak_role_to_domain(&role_data)?;
            Ok(Some(role))
        } else if response.status() == 404 {
            Ok(None)
        } else {
            let status = response.status();
            error!("Keycloak role fetch failed: {}", status);
            Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
        }
    }

    async fn find_by_name(&self, name: &str) -> AppResult<Option<Role>> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/roles/{}", self.base_url, self.realm, name);

        let response = self.http_client
            .get(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .send()
            .await
            .map_err(|e| {
                error!("Failed to fetch role by name {}: {}", name, e);
                AppError::InfrastructureError(format!("Failed to fetch role: {}", e))
            })?;

        if response.status().is_success() {
            let role_data: Value = response.json().await
                .map_err(|e| {
                    error!("Failed to parse role response: {}", e);
                    AppError::InfrastructureError("Failed to parse role data".to_string())
                })?;
            
            let role = self.map_keycloak_role_to_domain(&role_data)?;
            Ok(Some(role))
        } else if response.status() == 404 {
            Ok(None)
        } else {
            let status = response.status();
            error!("Keycloak role fetch failed: {}", status);
            Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
        }
    }

    async fn get_all_roles(&self) -> AppResult<Vec<Role>> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/roles", self.base_url, self.realm);

        let response = self.http_client
            .get(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .send()
            .await
            .map_err(|e| {
                error!("Failed to fetch all roles: {}", e);
                AppError::InfrastructureError(format!("Failed to fetch roles: {}", e))
            })?;

        if response.status().is_success() {
            let roles_data: Vec<Value> = response.json().await
                .map_err(|e| {
                    error!("Failed to parse roles response: {}", e);
                    AppError::InfrastructureError("Failed to parse roles data".to_string())
                })?;

            let mut roles = Vec::new();
            for role_data in roles_data {
                match self.map_keycloak_role_to_domain(&role_data) {
                    Ok(role) => roles.push(role),
                    Err(e) => {
                        warn!("Failed to map role data: {}", e);
                        continue;
                    }
                }
            }
            Ok(roles)
        } else {
            let status = response.status();
            error!("Keycloak roles fetch failed: {}", status);
            Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
        }
    }

    async fn get_user_roles(&self, user_id: &str) -> AppResult<Vec<Role>> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/users/{}/role-mappings/realm", self.base_url, self.realm, user_id);

        let response = self.http_client
            .get(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .send()
            .await
            .map_err(|e| {
                error!("Failed to fetch user roles for {}: {}", user_id, e);
                AppError::InfrastructureError(format!("Failed to fetch user roles: {}", e))
            })?;

        if response.status().is_success() {
            let roles_data: Vec<Value> = response.json().await
                .map_err(|e| {
                    error!("Failed to parse user roles response: {}", e);
                    AppError::InfrastructureError("Failed to parse user roles data".to_string())
                })?;

            let mut roles = Vec::new();
            for role_data in roles_data {
                match self.map_keycloak_role_to_domain(&role_data) {
                    Ok(role) => roles.push(role),
                    Err(e) => {
                        warn!("Failed to map user role data: {}", e);
                        continue;
                    }
                }
            }
            Ok(roles)
        } else if response.status() == 404 {
            Ok(Vec::new())
        } else {
            let status = response.status();
            error!("Keycloak user roles fetch failed: {}", status);
            Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
        }
    }

    async fn assign_roles(&self, user_id: &str, roles: &[String]) -> AppResult<()> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/users/{}/role-mappings/realm", self.base_url, self.realm, user_id);

        // First, get the role objects for the role names
        let mut role_objects = Vec::new();
        for role_name in roles {
if let Some(role) = RoleRepository::find_by_name(self, role_name).await? {
                role_objects.push(json!({
                    "id": role.id,
                    "name": role.name,
                }));
            } else {
                return Err(not_found_error("Role", role_name));
            }
        }

        info!("Assigning {} roles to user {}", role_objects.len(), user_id);

        let response = self.http_client
            .post(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .json(&role_objects)
            .send()
            .await
            .map_err(|e| {
                error!("Failed to assign roles to user {}: {}", user_id, e);
                AppError::InfrastructureError(format!("Failed to assign roles: {}", e))
            })?;

        if response.status().is_success() {
            info!("Roles assigned successfully to user: {}", user_id);
            Ok(())
        } else {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_default();
            error!("Keycloak role assignment failed: {} - {}", status, error_text);
            Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
        }
    }

    async fn remove_roles(&self, user_id: &str, roles: &[String]) -> AppResult<()> {
        let admin_token = self.get_admin_token().await?;
        let url = format!("{}/admin/realms/{}/users/{}/role-mappings/realm", self.base_url, self.realm, user_id);

        // First, get the role objects for the role names
        let mut role_objects = Vec::new();
        for role_name in roles {
if let Some(role) = RoleRepository::find_by_name(self, role_name).await? {
                role_objects.push(json!({
                    "id": role.id,
                    "name": role.name,
                }));
            } else {
                return Err(not_found_error("Role", role_name));
            }
        }

        info!("Removing {} roles from user {}", role_objects.len(), user_id);

        let response = self.http_client
            .delete(&url)
            .header("Authorization", format!("Bearer {}", admin_token))
            .header("Content-Type", "application/json")
            .json(&role_objects)
            .send()
            .await
            .map_err(|e| {
                error!("Failed to remove roles from user {}: {}", user_id, e);
                AppError::InfrastructureError(format!("Failed to remove roles: {}", e))
            })?;

        if response.status().is_success() {
            info!("Roles removed successfully from user: {}", user_id);
            Ok(())
        } else {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_default();
            error!("Keycloak role removal failed: {} - {}", status, error_text);
            Err(AppError::InfrastructureError(format!("Keycloak API error: {}", status)))
        }
    }
}

#[async_trait]
impl PermissionRepository for KeycloakClient {
    async fn find_by_id(&self, _id: &str) -> AppResult<Option<Permission>> {
        // Keycloak doesn't have a direct permissions API in the same way
        // Permissions are typically derived from roles and scopes
        warn!("Permission by ID not fully implemented for Keycloak");
        Ok(None)
    }

    async fn find_by_name(&self, _name: &str) -> AppResult<Option<Permission>> {
        // Keycloak doesn't have a direct permissions API
        warn!("Permission by name not fully implemented for Keycloak");
        Ok(None)
    }

    async fn get_user_permissions(&self, user_id: &str) -> AppResult<Vec<Permission>> {
        // In Keycloak, permissions are typically derived from roles
        // For simplicity, we'll create permissions based on role names
        let roles = self.get_user_roles(user_id).await?;
        
        let permissions = roles.into_iter().map(|role| {
            Permission::new(
                role.id.clone(),
                format!("role:{}", role.name),
                Some(format!("Permission derived from role: {}", role.name)),
                Some("role".to_string()),
            )
        }).collect();

        Ok(permissions)
    }

    async fn has_permission(&self, user_id: &str, permission: &str) -> AppResult<bool> {
        // Check if the user has a role that matches the permission pattern
        let roles = self.get_user_roles(user_id).await?;
        
        // Simple check: if permission starts with "role:", check if user has that role
        if let Some(role_name) = permission.strip_prefix("role:") {
            return Ok(roles.iter().any(|role| role.name == role_name));
        }

        // For other permissions, we'd need more complex logic based on Keycloak's permission system
        Ok(false)
    }
}