use crate::shared::errors::AppError;
use sqlx::postgres::{PgPool, PgPoolOptions};

#[derive(Clone, Debug)]
pub struct Database {
    pub pool: PgPool,
}

impl Database {
    pub async fn new(database_url: &str) -> Result<Self, AppError> {
        let pool = PgPoolOptions::new()
            .max_connections(10)
            .connect(database_url)
            .await
            .map_err(|e| AppError::Config(format!("Failed to connect to database: {}", e)))?;

        // Test the connection
        sqlx::query("SELECT 1")
            .execute(&pool)
            .await
            .map_err(|e| AppError::Config(format!("Database connection test failed: {}", e)))?;

        log::info!("Database connection established successfully");

        Ok(Database { pool })
    }

    pub fn get_pool(&self) -> &PgPool {
        &self.pool
    }
}
