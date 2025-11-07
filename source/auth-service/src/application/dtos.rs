use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
use crate::domain::{User, Role, Permission, Token, TokenValidation, TokenIntrospection};

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct UserDto {
    pub id: String,
    pub email: String,
    pub username: String,
    pub first_name: String,
    pub last_name: String,
    pub full_name: String,
    pub enabled: bool,
    pub email_verified: bool,
    pub created_at: Option<i64>,
    pub updated_at: Option<i64>,
}

impl UserDto {
    pub fn from_domain(user: User) -> Self {
        // Clone the values to avoid partial move
        let first_name = user.first_name.clone();
        let last_name = user.last_name.clone();
        let full_name = user.get_full_name();
        
        Self {
            id: user.id,
            email: user.email,
            username: user.username,
            first_name,
            last_name,
            full_name,
            enabled: user.enabled,
            email_verified: user.email_verified,
            created_at: user.created_at,
            updated_at: user.updated_at,
        }
    }
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct RoleDto {
    pub id: String,
    pub name: String,
    pub description: Option<String>,
    pub composite: bool,
    pub client_role: bool,
}

impl RoleDto {
    pub fn from_domain(role: Role) -> Self {
        Self {
            id: role.id,
            name: role.name,
            description: role.description,
            composite: role.composite,
            client_role: role.client_role,
        }
    }

    pub fn from_domain_vec(roles: Vec<Role>) -> Vec<Self> {
        roles.into_iter().map(Self::from_domain).collect()
    }
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct PermissionDto {
    pub id: String,
    pub name: String,
    pub description: Option<String>,
    pub resource_type: Option<String>,
    pub scopes: Vec<String>,
}

impl PermissionDto {
    pub fn from_domain(permission: Permission) -> Self {
        Self {
            id: permission.id,
            name: permission.name,
            description: permission.description,
            resource_type: permission.resource_type,
            scopes: permission.scopes,
        }
    }

    pub fn from_domain_vec(permissions: Vec<Permission>) -> Vec<Self> {
        permissions.into_iter().map(Self::from_domain).collect()
    }
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct TokenDto {
    pub access_token: String,
    pub refresh_token: String,
    pub expires_in: i64,
    pub refresh_expires_in: i64,
    pub token_type: String,
    pub scope: Option<String>,
}

impl TokenDto {
    pub fn from_domain(token: Token) -> Self {
        Self {
            access_token: token.access_token,
            refresh_token: token.refresh_token,
            expires_in: token.expires_in,
            refresh_expires_in: token.refresh_expires_in,
            token_type: token.token_type,
            scope: token.scope,
        }
    }
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct LoginResponse {
    pub access_token: String,
    pub refresh_token: String,
    pub expires_in: i64,
    pub token_type: String,
    pub user: UserDto,
}

impl LoginResponse {
    pub fn new(token: Token, user: User) -> Self {
        Self {
            access_token: token.access_token,
            refresh_token: token.refresh_token,
            expires_in: token.expires_in,
            token_type: token.token_type,
            user: UserDto::from_domain(user),
        }
    }
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct TokenValidationResponse {
    pub valid: bool,
    pub user_id: Option<String>,
    pub username: Option<String>,
    pub email: Option<String>,
    pub roles: Vec<String>,
    pub permissions: Vec<String>,
    pub expires_at: Option<i64>,
}

impl TokenValidationResponse {
    pub fn from_domain(validation: TokenValidation) -> Self {
        Self {
            valid: validation.valid,
            user_id: validation.user_id,
            username: validation.username,
            email: validation.email,
            roles: validation.roles,
            permissions: validation.permissions,
            expires_at: validation.expires_at,
        }
    }

    // Update these helper methods to use correct TokenIntrospection fields
    pub fn valid(introspection: TokenIntrospection) -> Self {
        Self {
            valid: introspection.active,
            user_id: introspection.sub, // Use 'sub' field for user ID
            username: introspection.username,
            email: introspection.email,
            roles: introspection.realm_access.map(|ra| ra.roles).unwrap_or_default(),
            permissions: Vec::new(), // Keycloak doesn't provide permissions directly in introspection
            expires_at: introspection.exp, // Use 'exp' field for expiration
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
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct UserResponse {
    pub user: UserDto,
    pub roles: Vec<RoleDto>,
    pub permissions: Vec<PermissionDto>,
}

impl UserResponse {
    pub fn new(user: UserDto, roles: Vec<RoleDto>, permissions: Vec<PermissionDto>) -> Self {
        Self {
            user,
            roles,
            permissions,
        }
    }
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct RoleResponse {
    pub role: RoleDto,
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct PermissionResponse {
    pub permission: PermissionDto,
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct ListUsersResponse {
    pub users: Vec<UserDto>,
    pub total: u64,
    pub page: u32,
    pub size: u32,
    pub total_pages: u32,
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct AssignRolesResponse {
    pub user_id: String,
    pub assigned_roles: Vec<String>,
    pub message: String,
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct CheckPermissionResponse {
    pub has_permission: bool,
    pub user_id: String,
    pub permission: String,
}