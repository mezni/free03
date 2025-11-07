use async_trait::async_trait;
use crate::shared::result::AppResult;
use super::{User, CreateUserRequest, Token, TokenValidation, UserEntity};

/// Domain service for authentication business logic
/// This contains business rules that don't naturally fit in entities or value objects
#[async_trait]
pub trait AuthService: Send + Sync {
    /// Validate user credentials and return user if valid
    async fn authenticate_user(&self, username: &str, password: &str) -> AppResult<User>;
    
    /// Register a new user with validation rules
    async fn register_user(&self, user_request: &CreateUserRequest) -> AppResult<User>;
    
    /// Generate tokens for a user
    async fn generate_tokens(&self, user: &User) -> AppResult<Token>;
    
    /// Validate and introspect a token
    async fn validate_token(&self, token: &str) -> AppResult<TokenValidation>;
    
    /// Refresh an access token using refresh token
    async fn refresh_token(&self, refresh_token: &str) -> AppResult<Token>;
    
    /// Logout user by invalidating tokens
    async fn logout(&self, refresh_token: &str) -> AppResult<()>;
    
    /// Check if user has specific permission
    async fn check_permission(&self, user_id: &str, permission: &str) -> AppResult<bool>;
    
    /// Get user entity with roles and permissions
    async fn get_user_entity(&self, user_id: &str) -> AppResult<UserEntity>;
}

/// Password service for password hashing and verification
#[async_trait]
pub trait PasswordService: Send + Sync {
    /// Hash a password
    async fn hash_password(&self, password: &str) -> AppResult<String>;
    
    /// Verify a password against a hash
    async fn verify_password(&self, password: &str, hash: &str) -> AppResult<bool>;
    
    /// Validate password strength
    fn validate_password_strength(&self, password: &str) -> AppResult<()>;
}

/// Token service for JWT token operations
#[async_trait]
pub trait TokenService: Send + Sync {
    /// Generate access token for user
    async fn generate_access_token(&self, user: &User) -> AppResult<String>;
    
    /// Generate refresh token for user
    async fn generate_refresh_token(&self, user: &User) -> AppResult<String>;
    
    /// Validate token and extract claims
    async fn validate_token(&self, token: &str) -> AppResult<super::token::TokenClaims>;
    
    /// Decode token without validation (for introspection)
    async fn decode_token(&self, token: &str) -> AppResult<serde_json::Value>;
}