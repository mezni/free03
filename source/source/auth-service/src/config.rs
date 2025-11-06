use serde::Deserialize;
use std::env;

#[derive(Debug, Clone)]
pub struct AppConfig {
    pub server_host: String,
    pub server_port: u16,

    pub keycloak_url: String,
    pub keycloak_realm: String,
    pub keycloak_client_id: String,
    pub keycloak_client_secret: String,

    pub cache_ttl_seconds: u64,
}

impl AppConfig {
    pub fn from_env() -> Self {
        dotenv::dotenv().ok(); // load .env if exists

        let server_host = env::var("SERVER_HOST").unwrap_or_else(|_| "0.0.0.0".to_string());
        let server_port = env::var("SERVER_PORT")
            .unwrap_or_else(|_| "8081".to_string())
            .parse()
            .expect("SERVER_PORT must be a number");

        let keycloak_url = env::var("KEYCLOAK_URL").unwrap_or_else(|_| "http://localhost:8080".to_string());
        let keycloak_realm = env::var("KEYCLOAK_REALM").unwrap_or_else(|_| "myrealm".to_string());
        let keycloak_client_id = env::var("KEYCLOAK_CLIENT_ID").unwrap_or_else(|_| "auth-service".to_string());
        let keycloak_client_secret = env::var("KEYCLOAK_CLIENT_SECRET")
            .unwrap_or_else(|_| "AuthServiceSecret123!".to_string());

        let cache_ttl_seconds = env::var("CACHE_TTL_SECONDS")
            .unwrap_or_else(|_| "300".to_string())
            .parse()
            .expect("CACHE_TTL_SECONDS must be a number");

        AppConfig {
            server_host,
            server_port,
            keycloak_url,
            keycloak_realm,
            keycloak_client_id,
            keycloak_client_secret,
            cache_ttl_seconds,
        }
    }
}
