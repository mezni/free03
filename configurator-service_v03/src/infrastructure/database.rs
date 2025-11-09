use sqlx::{Pool, Postgres, postgres::PgPoolOptions};
use std::time::Duration;
use crate::shared::errors::AppError;

pub struct DbPoolWrapper {
    pub pool: Pool<Postgres>,
}

impl DbPoolWrapper {
    pub async fn new(database_url: &str) -> Result<Self, AppError> {
        let pool = PgPoolOptions::new()
            .max_connections(10)
            .acquire_timeout(Duration::from_secs(5))
            .connect(database_url)
            .await
            .map_err(|e| AppError::DbError(e.to_string()))?;

        Ok(Self { pool })
    }
}
