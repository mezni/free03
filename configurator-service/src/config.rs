use serde::Deserialize;

#[derive(Debug, Deserialize, Clone)]
pub struct Config {
    #[serde(default = "default_host")]
    pub host: String,
    
    #[serde(default = "default_port")]
    pub port: u16,
    
    #[serde(default = "default_database_url")]
    pub database_url: String,
    
    #[serde(default = "default_cache_capacity")]
    pub cache_capacity: u64,
    
    #[serde(default = "default_cache_ttl")]
    pub cache_ttl_seconds: u64,
}

fn default_host() -> String {
    "0.0.0.0".to_string()
}

fn default_port() -> u16 {
    8080
}

fn default_database_url() -> String {
    "postgresql://postgres:password@localhost:5432/ev_db".to_string()
}

fn default_cache_capacity() -> u64 {
    10_000
}

fn default_cache_ttl() -> u64 {
    300 // 5 minutes
}

impl Config {
    pub fn from_env() -> Result<Self, config::ConfigError> {
        let config = config::Config::builder()
            .add_source(config::Environment::with_prefix("APP"))
            .build()?;
            
        config.try_deserialize()
    }
    
    pub fn server_address(&self) -> String {
        format!("{}:{}", self.host, self.port)
    }
}

impl Default for Config {
    fn default() -> Self {
        Self {
            host: default_host(),
            port: default_port(),
            database_url: default_database_url(),
            cache_capacity: default_cache_capacity(),
            cache_ttl_seconds: default_cache_ttl(),
        }
    }
}