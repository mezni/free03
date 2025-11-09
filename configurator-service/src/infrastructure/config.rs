use crate::shared::errors::AppError;
use serde::Deserialize;

#[derive(Debug, Clone, Deserialize)]
pub struct Config {
    pub database_url: String,
    pub host: String,
    pub port: u16,
    pub log_level: String,
    pub max_connections: u32,
}

impl Config {
    pub fn from_env() -> Result<Self, AppError> {
        let database_url = std::env::var("DATABASE_URL")
            .map_err(|_| AppError::Config("DATABASE_URL not set".to_string()))?;

        let host = std::env::var("HOST").unwrap_or_else(|_| "127.0.0.1".to_string());

        let port = std::env::var("PORT")
            .unwrap_or_else(|_| "8080".to_string())
            .parse()
            .map_err(|_| AppError::Config("Invalid PORT value".to_string()))?;

        let log_level = std::env::var("LOG_LEVEL").unwrap_or_else(|_| "info".to_string());

        let max_connections = std::env::var("DATABASE_MAX_CONNECTIONS")
            .unwrap_or_else(|_| "10".to_string())
            .parse()
            .map_err(|_| AppError::Config("Invalid DATABASE_MAX_CONNECTIONS value".to_string()))?;

        Ok(Config {
            database_url,
            host,
            port,
            log_level,
            max_connections,
        })
    }
}
