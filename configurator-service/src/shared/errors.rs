use serde::Serialize;
use utoipa::ToSchema;

#[derive(Debug, Serialize, ToSchema)]
pub struct AppError {
    pub message: String,
    pub error_type: ErrorType,
}

#[derive(Debug, Serialize, ToSchema)]
pub enum ErrorType {
    Validation,
    Database,
    NotFound,
    Internal,
}

impl AppError {
    pub fn validation(message: String) -> Self {
        Self {
            message,
            error_type: ErrorType::Validation,
        }
    }
    
    pub fn database(message: String) -> Self {
        Self {
            message,
            error_type: ErrorType::Database,
        }
    }
    
    pub fn not_found(message: String) -> Self {
        Self {
            message,
            error_type: ErrorType::NotFound,
        }
    }
    
    pub fn internal(message: String) -> Self {
        Self {
            message,
            error_type: ErrorType::Internal,
        }
    }
}