use thiserror::Error;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("Configuration Error: {0}")]
    Config(String),

    #[error("Database Error: {0}")]
    Database(String),

    #[error("Internal Server Error")]
    Internal,
}
