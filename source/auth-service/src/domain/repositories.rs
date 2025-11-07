use async_trait::async_trait;
use crate::shared::result::AppResult;
use super::{User, Role, Permission, CreateUserRequest, Token, UserEntity};

/// Repository for user aggregate operations
#[async_trait]
pub trait UserRepository: Send + Sync {
    /// Find user by ID
    async fn find_by_id(&self, id: &str) -> AppResult<Option<User>>;
    
    /// Find user by username
    async fn find_by_username(&self, username: &str) -> AppResult<Option<User>>;
    
    /// Find user by email
    async fn find_by_email(&self, email: &str) -> AppResult<Option<User>>;
    
    /// Create a new user
    async fn create_user(&self, user: &CreateUserRequest) -> AppResult<User>;
    
    /// Update user information
    async fn update_user(&self, user: &User) -> AppResult<User>;
    
    /// Delete user by ID
    async fn delete_user(&self, id: &str) -> AppResult<()>;
    
    /// Check if username exists
    async fn username_exists(&self, username: &str) -> AppResult<bool>;
    
    /// Check if email exists
    async fn email_exists(&self, email: &str) -> AppResult<bool>;
    
    /// Validate user credentials
    async fn validate_credentials(&self, username: &str, password: &str) -> AppResult<bool>;
}

/// Repository for role operations
#[async_trait]
pub trait RoleRepository: Send + Sync {
    /// Find role by ID
    async fn find_by_id(&self, id: &str) -> AppResult<Option<Role>>;
    
    /// Find role by name
    async fn find_by_name(&self, name: &str) -> AppResult<Option<Role>>;
    
    /// Get all roles
    async fn get_all_roles(&self) -> AppResult<Vec<Role>>;
    
    /// Get user roles
    async fn get_user_roles(&self, user_id: &str) -> AppResult<Vec<Role>>;
    
    /// Assign roles to user
    async fn assign_roles(&self, user_id: &str, roles: &[String]) -> AppResult<()>;
    
    /// Remove roles from user
    async fn remove_roles(&self, user_id: &str, roles: &[String]) -> AppResult<()>;
}

/// Repository for permission operations
#[async_trait]
pub trait PermissionRepository: Send + Sync {
    /// Find permission by ID
    async fn find_by_id(&self, id: &str) -> AppResult<Option<Permission>>;
    
    /// Find permission by name
    async fn find_by_name(&self, name: &str) -> AppResult<Option<Permission>>;
    
    /// Get user permissions
    async fn get_user_permissions(&self, user_id: &str) -> AppResult<Vec<Permission>>;
    
    /// Check if user has specific permission
    async fn has_permission(&self, user_id: &str, permission: &str) -> AppResult<bool>;
}

/// Repository for token operations
#[async_trait]
pub trait TokenRepository: Send + Sync {
    /// Generate tokens for user
    async fn generate_token(&self, username: &str, password: &str) -> AppResult<Token>;
    
    /// Refresh access token
    async fn refresh_token(&self, refresh_token: &str) -> AppResult<Token>;
    
    /// Validate token
    async fn validate_token(&self, token: &str) -> AppResult<bool>;
    
    /// Introspect token for detailed information
    async fn introspect_token(&self, token: &str) -> AppResult<super::token::TokenIntrospection>;
    
    /// Logout user by invalidating tokens
    async fn logout(&self, refresh_token: &str) -> AppResult<()>;
    
    /// Store token in cache (if needed)
    async fn store_token(&self, token: &Token, user_id: &str) -> AppResult<()>;
    
    /// Revoke token
    async fn revoke_token(&self, token: &str) -> AppResult<()>;
}

/// Aggregate repository for user entity operations
#[async_trait]
pub trait UserEntityRepository: Send + Sync {
    /// Get user entity with roles and permissions
    async fn get_user_entity(&self, user_id: &str) -> AppResult<UserEntity>;
    
    /// Save user entity
    async fn save_user_entity(&self, user_entity: &UserEntity) -> AppResult<()>;
}