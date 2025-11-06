use actix_web::{HttpResponse, ResponseError};
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Keycloak error: {0}")]
    KeycloakError(String),

    #[error("Cache error: {0}")]
    CacheError(String),

    #[error("Unauthorized")]
    Unauthorized,
}

impl ResponseError for AppError {
    fn error_response(&self) -> HttpResponse {
        match self {
            AppError::KeycloakError(msg) => HttpResponse::InternalServerError().body(msg.clone()),
            AppError::CacheError(msg) => HttpResponse::InternalServerError().body(msg.clone()),
            AppError::Unauthorized => HttpResponse::Unauthorized().body("Unauthorized"),
        }
    }
}
