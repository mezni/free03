use actix_web::{HttpResponse, ResponseError};
use serde::Serialize;
use std::fmt;

#[derive(Debug, Serialize)]
pub struct ErrorResponse {
    pub error: String,
    pub message: String,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub details: Option<String>,
}

#[derive(Debug)]
pub enum AppError {
    // Domain errors
    DomainError(String),
    ValidationError(String),
    
    // Authentication & Authorization errors
    AuthError(String),
    Unauthorized(String),
    Forbidden(String),
    
    // Infrastructure errors
    InfrastructureError(String),
    ExternalServiceError(String),
    
    // Application errors
    NotFound(String),
    Conflict(String),
    BadRequest(String),
}

impl fmt::Display for AppError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            AppError::DomainError(msg) => write!(f, "Domain error: {}", msg),
            AppError::ValidationError(msg) => write!(f, "Validation error: {}", msg),
            AppError::AuthError(msg) => write!(f, "Authentication error: {}", msg),
            AppError::Unauthorized(msg) => write!(f, "Unauthorized: {}", msg),
            AppError::Forbidden(msg) => write!(f, "Forbidden: {}", msg),
            AppError::InfrastructureError(msg) => write!(f, "Infrastructure error: {}", msg),
            AppError::ExternalServiceError(msg) => write!(f, "External service error: {}", msg),
            AppError::NotFound(msg) => write!(f, "Not found: {}", msg),
            AppError::Conflict(msg) => write!(f, "Conflict: {}", msg),
            AppError::BadRequest(msg) => write!(f, "Bad request: {}", msg),
        }
    }
}

impl ResponseError for AppError {
    fn error_response(&self) -> HttpResponse {
        let (status, message) = match self {
            AppError::DomainError(msg) => (actix_web::http::StatusCode::INTERNAL_SERVER_ERROR, msg),
            AppError::ValidationError(msg) => (actix_web::http::StatusCode::BAD_REQUEST, msg),
            AppError::AuthError(msg) => (actix_web::http::StatusCode::UNAUTHORIZED, msg),
            AppError::Unauthorized(msg) => (actix_web::http::StatusCode::UNAUTHORIZED, msg),
            AppError::Forbidden(msg) => (actix_web::http::StatusCode::FORBIDDEN, msg),
            AppError::InfrastructureError(msg) => (actix_web::http::StatusCode::SERVICE_UNAVAILABLE, msg),
            AppError::ExternalServiceError(msg) => (actix_web::http::StatusCode::BAD_GATEWAY, msg),
            AppError::NotFound(msg) => (actix_web::http::StatusCode::NOT_FOUND, msg),
            AppError::Conflict(msg) => (actix_web::http::StatusCode::CONFLICT, msg),
            AppError::BadRequest(msg) => (actix_web::http::StatusCode::BAD_REQUEST, msg),
        };

        HttpResponse::build(status).json(ErrorResponse {
            error: status.to_string(),
            message: message.clone(),
            details: None,
        })
    }
}

// Common error conversions
impl From<reqwest::Error> for AppError {
    fn from(err: reqwest::Error) -> Self {
        if err.is_timeout() {
            AppError::ExternalServiceError("Request timeout".to_string())
        } else if err.is_connect() {
            AppError::ExternalServiceError("Connection failed".to_string())
        } else {
            AppError::ExternalServiceError(err.to_string())
        }
    }
}

impl From<serde_json::Error> for AppError {
    fn from(err: serde_json::Error) -> Self {
        AppError::ValidationError(format!("JSON serialization error: {}", err))
    }
}

impl From<validator::ValidationErrors> for AppError {
    fn from(err: validator::ValidationErrors) -> Self {
        let messages: Vec<String> = err
            .field_errors()
            .iter()
            .map(|(field, errors)| {
                let error_messages: Vec<String> = errors
                    .iter()
                    .map(|e| e.message.as_ref().map(|m| m.to_string()).unwrap_or_default())
                    .collect();
                format!("{}: {}", field, error_messages.join(", "))
            })
            .collect();
        
        AppError::ValidationError(messages.join("; "))
    }
}

impl From<std::env::VarError> for AppError {
    fn from(err: std::env::VarError) -> Self {
        AppError::InfrastructureError(format!("Environment variable error: {}", err))
    }
}

impl From<config::ConfigError> for AppError {
    fn from(err: config::ConfigError) -> Self {
        AppError::InfrastructureError(format!("Configuration error: {}", err))
    }
}