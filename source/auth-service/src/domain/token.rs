use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Token {
    pub access_token: String,
    pub refresh_token: String,
    pub expires_in: i64,
    pub refresh_expires_in: i64,
    pub token_type: String,
    pub scope: Option<String>,
    pub session_state: Option<String>,
}

impl Token {
    pub fn new(
        access_token: String,
        refresh_token: String,
        expires_in: i64,
        refresh_expires_in: i64,
        token_type: String,
    ) -> Self {
        Self {
            access_token,
            refresh_token,
            expires_in,
            refresh_expires_in,
            token_type,
            scope: None,
            session_state: None,
        }
    }

    pub fn is_expired(&self) -> bool {
        // This would typically decode the token and check expiration
        // For now, we assume the token is valid if we have it
        false
    }

    pub fn expires_at(&self) -> DateTime<Utc> {
        Utc::now() + chrono::Duration::seconds(self.expires_in)
    }

    pub fn refresh_expires_at(&self) -> DateTime<Utc> {
        Utc::now() + chrono::Duration::seconds(self.refresh_expires_in)
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TokenValidation {
    pub valid: bool,
    pub user_id: Option<String>,
    pub username: Option<String>,
    pub email: Option<String>,
    pub roles: Vec<String>,
    pub permissions: Vec<String>,
    pub expires_at: Option<i64>,
}

impl TokenValidation {
    pub fn valid(user_id: String, username: String, email: String, roles: Vec<String>, permissions: Vec<String>, expires_at: i64) -> Self {
        Self {
            valid: true,
            user_id: Some(user_id),
            username: Some(username),
            email: Some(email),
            roles,
            permissions,
            expires_at: Some(expires_at),
        }
    }

    pub fn invalid() -> Self {
        Self {
            valid: false,
            user_id: None,
            username: None,
            email: None,
            roles: Vec::new(),
            permissions: Vec::new(),
            expires_at: None,
        }
    }

    pub fn has_role(&self, role: &str) -> bool {
        self.roles.iter().any(|r| r == role)
    }

    pub fn has_permission(&self, permission: &str) -> bool {
        self.permissions.iter().any(|p| p == permission)
    }

    pub fn is_admin(&self) -> bool {
        self.has_role("admin") || self.has_role("super_admin")
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TokenIntrospection {
    pub active: bool,
    pub sub: Option<String>,
    pub username: Option<String>,
    pub email: Option<String>,
    pub name: Option<String>,
    pub given_name: Option<String>,
    pub family_name: Option<String>,
    pub preferred_username: Option<String>,
    pub realm_access: Option<RealmAccess>,
    pub resource_access: Option<serde_json::Value>,
    pub scope: Option<String>,
    pub exp: Option<i64>,
    pub iat: Option<i64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RealmAccess {
    pub roles: Vec<String>,
}

impl TokenIntrospection {
    pub fn from_json_value(value: serde_json::Value) -> Self {
        serde_json::from_value(value).unwrap_or_else(|_| Self::inactive())
    }

    pub fn inactive() -> Self {
        Self {
            active: false,
            sub: None,
            username: None,
            email: None,
            name: None,
            given_name: None,
            family_name: None,
            preferred_username: None,
            realm_access: None,
            resource_access: None,
            scope: None,
            exp: None,
            iat: None,
        }
    }

    pub fn get_roles(&self) -> Vec<String> {
        self.realm_access
            .as_ref()
            .map(|ra| ra.roles.clone())
            .unwrap_or_default()
    }

    pub fn get_permissions(&self) -> Vec<String> {
        // Extract permissions from resource_access or scope
        if let Some(scope) = &self.scope {
            scope.split(' ').map(|s| s.to_string()).collect()
        } else {
            Vec::new()
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TokenClaims {
    pub sub: String,
    pub preferred_username: String,
    pub email: String,
    pub given_name: Option<String>,
    pub family_name: Option<String>,
    pub realm_access: RealmAccess,
    pub exp: i64,
    pub iat: i64,
}