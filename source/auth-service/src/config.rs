// src/config.rs
use serde::Deserialize;
use std::env;

#[derive(Debug, Clone, Deserialize)]
pub struct ServerConfig {
    pub host: String,
    pub port: u16,
}

#[derive(Debug, Clone, Deserialize)]
pub struct KeycloakConfig {
    pub url: String,
    pub realm: String,
    pub client_id: String,
    pub client_secret: String,
    pub admin_username: Option<String>,
    pub admin_password: Option<String>,
}

#[derive(Debug, Clone, Deserialize)]
pub struct DatabaseConfig {
    pub url: String,
    pub max_connections: u32,
}

#[derive(Debug, Clone, Deserialize)]
pub struct CacheConfig {
    pub redis_url: Option<String>,
    pub ttl_seconds: u64,
}

#[derive(Debug, Clone, Deserialize)]
pub struct JwtConfig {
    pub secret: String,
    pub expiration_hours: i64,
}

#[derive(Debug, Clone, Deserialize)]
pub struct LogConfig {
    pub level: String,
    pub format: String,
}

#[derive(Debug, Clone, Deserialize)]
pub struct Config {
    pub server: ServerConfig,
    pub keycloak: KeycloakConfig,
    pub database: DatabaseConfig,
    pub cache: CacheConfig,
    pub jwt: JwtConfig,
    pub log: LogConfig,
}

impl Config {
    pub fn from_env() -> Result<Self, config::ConfigError> {
        let environment = env::var("APP_ENV").unwrap_or_else(|_| "development".into());
        
        let config = config::Config::builder()
            .add_source(config::File::with_name("config/default").required(false))
            .add_source(config::File::with_name(&format!("config/{}", environment)).required(false))
            .add_source(config::Environment::with_prefix("APP").separator("__"))
            .build()?;

        config.try_deserialize()
    }

    pub fn server_address(&self) -> String {
        format!("{}:{}", self.server.host, self.server.port)
    }
}

impl Default for Config {
    fn default() -> Self {
        Self {
            server: ServerConfig {
                host: "127.0.0.1".to_string(),
                port: 8080,
            },
            keycloak: KeycloakConfig {
                url: "http://localhost:8080".to_string(),
                realm: "master".to_string(),
                client_id: "admin-cli".to_string(),
                client_secret: "".to_string(),
                admin_username: None,
                admin_password: None,
            },
            database: DatabaseConfig {
                url: "postgres://user:pass@localhost:5432/auth".to_string(),
                max_connections: 10,
            },
            cache: CacheConfig {
                redis_url: Some("redis://localhost:6379".to_string()),
                ttl_seconds: 3600,
            },
            jwt: JwtConfig {
                secret: "secret".to_string(),
                expiration_hours: 24,
            },
            log: LogConfig {
                level: "info".to_string(),
                format: "text".to_string(),
            },
        }
    }
}