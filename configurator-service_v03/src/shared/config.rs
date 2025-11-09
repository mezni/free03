use dotenvy::dotenv;
use std::env;

#[derive(Debug, Clone)]
pub struct Config {
    pub server_host: String,
    pub server_port: u16,
    pub database_url: String,
    pub cache_capacity: u64,
}

impl Config {
    pub fn from_env() -> Self {
        dotenv().ok();

        Self {
            server_host: env::var("SERVER_HOST").unwrap_or_else(|_| "0.0.0.0".to_string()),
            server_port: env::var("SERVER_PORT")
                .unwrap_or_else(|_| "8080".to_string())
                .parse()
                .expect("SERVER_PORT must be a number"),
            database_url: env::var("DATABASE_URL").expect("DATABASE_URL must be set"),
            cache_capacity: env::var("CACHE_CAPACITY")
                .unwrap_or_else(|_| "10000".to_string())
                .parse()
                .expect("CACHE_CAPACITY must be a number"),
        }
    }
}
