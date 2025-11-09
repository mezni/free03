use thiserror::Error;
use actix_web::{HttpResponse, ResponseError};

#[derive(Debug, Error)]
pub enum AppError {
    #[error("Database error: {0}")]
    DbError(String),
    #[error("Not found: {0}")]
    NotFound(String),
    #[error("Validation failed: {0}")]
    Validation(String),
    #[error("Internal error: {0}")]
    Internal(String),
}

impl ResponseError for AppError {
    fn error_response(&self) -> HttpResponse {
        match self {
            AppError::NotFound(msg) => HttpResponse::NotFound().body(msg),
            AppError::Validation(msg) => HttpResponse::BadRequest().body(msg),
            _ => HttpResponse::InternalServerError().body(self.to_string()),
        }
    }
}
