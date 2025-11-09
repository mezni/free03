use actix_web::{HttpResponse, ResponseError};
use serde::Serialize;
use serde_json::json;
use thiserror::Error;
use utoipa::ToSchema;

#[derive(Error, Debug, Serialize, ToSchema)]
#[serde(tag = "type", content = "details")]
pub enum AppError {
    #[error("Database error: {0}")]
    Database(String),

    #[error("Validation error: {0}")]
    Validation(String),

    #[error("Not found: {0}")]
    NotFound(String),

    #[error("Unauthorized: {0}")]
    Unauthorized(String),

    #[error("Internal server error")]
    Internal,

    #[error("Configuration error: {0}")]
    Config(String),

    #[error("Serialization error: {0}")]
    Serialization(String),
}

impl ResponseError for AppError {
    fn error_response(&self) -> HttpResponse {
        match self {
            AppError::Database(_) => HttpResponse::InternalServerError().json(json!({
                "error": "Database error occurred"
            })),
            AppError::Validation(msg) => HttpResponse::BadRequest().json(json!({
                "error": "Validation failed",
                "message": msg
            })),
            AppError::NotFound(msg) => HttpResponse::NotFound().json(json!({
                "error": "Resource not found",
                "message": msg
            })),
            AppError::Unauthorized(msg) => HttpResponse::Unauthorized().json(json!({
                "error": "Unauthorized",
                "message": msg
            })),
            AppError::Internal => HttpResponse::InternalServerError().json(json!({
                "error": "Internal server error"
            })),
            AppError::Config(msg) => HttpResponse::InternalServerError().json(json!({
                "error": "Configuration error",
                "message": msg
            })),
            AppError::Serialization(_) => HttpResponse::InternalServerError().json(json!({
                "error": "Serialization error"
            })),
        }
    }
}

// Optional: convert from external errors to AppError
impl From<sqlx::Error> for AppError {
    fn from(err: sqlx::Error) -> Self {
        AppError::Database(err.to_string())
    }
}

impl From<serde_json::Error> for AppError {
    fn from(err: serde_json::Error) -> Self {
        AppError::Serialization(err.to_string())
    }
}

impl From<String> for AppError {
    fn from(value: String) -> Self {
        AppError::Validation(value)
    }
}

impl From<&str> for AppError {
    fn from(value: &str) -> Self {
        AppError::Validation(value.to_string())
    }
}
