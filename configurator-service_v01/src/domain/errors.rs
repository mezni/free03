use crate::shared::errors::AppError;

pub type DomainResult<T> = Result<T, AppError>;

pub fn validation_error(message: &str) -> AppError {
    AppError::validation(message.to_string())
}