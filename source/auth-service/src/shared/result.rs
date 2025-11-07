pub use crate::shared::error::AppError;

pub type AppResult<T> = std::result::Result<T, AppError>;

/// Extension trait for Result to easily convert to AppResult
pub trait ResultExt<T> {
    fn domain_err(self, msg: &str) -> AppResult<T>;
    fn auth_err(self, msg: &str) -> AppResult<T>;
    fn not_found_err(self, msg: &str) -> AppResult<T>;
    fn validation_err(self, msg: &str) -> AppResult<T>;
}

impl<T, E: std::fmt::Display> ResultExt<T> for Result<T, E> {
    fn domain_err(self, msg: &str) -> AppResult<T> {
        self.map_err(|e| AppError::DomainError(format!("{}: {}", msg, e)))
    }

    fn auth_err(self, msg: &str) -> AppResult<T> {
        self.map_err(|e| AppError::AuthError(format!("{}: {}", msg, e)))
    }

    fn not_found_err(self, msg: &str) -> AppResult<T> {
        self.map_err(|e| AppError::NotFound(format!("{}: {}", msg, e)))
    }

    fn validation_err(self, msg: &str) -> AppResult<T> {
        self.map_err(|e| AppError::ValidationError(format!("{}: {}", msg, e)))
    }
}

/// Helper function to create validation errors
pub fn validation_error(msg: &str) -> AppError {
    AppError::ValidationError(msg.to_string())
}

/// Helper function to create not found errors
pub fn not_found_error(resource: &str, id: &str) -> AppError {
    AppError::NotFound(format!("{} with id '{}' not found", resource, id))
}

/// Helper function to create unauthorized errors
pub fn unauthorized_error(msg: &str) -> AppError {
    AppError::Unauthorized(msg.to_string())
}

/// Helper function to create forbidden errors
pub fn forbidden_error(msg: &str) -> AppError {
    AppError::Forbidden(msg.to_string())
}