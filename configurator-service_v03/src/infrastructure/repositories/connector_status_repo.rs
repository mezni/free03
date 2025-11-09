use crate::domain::connector_status::ConnectorStatus;
use crate::shared::errors::AppError;
use sqlx::PgPool;
use std::sync::Arc;
use moka::future::Cache;
use tracing::{info, debug};

#[derive(Clone)]
pub struct ConnectorStatusRepository {
    pool: PgPool,
    cache: Option<Arc<Cache<String, Vec<ConnectorStatus>>>>,
}

impl ConnectorStatusRepository {
    pub fn new(pool: PgPool, cache: Option<Arc<Cache<String, Vec<ConnectorStatus>>>>) -> Self {
        if let Some(ref c) = cache {
            debug!("ConnectorStatusRepository using shared cache with {} entries", c.entry_count());
        } else {
            debug!("ConnectorStatusRepository initialized without cache");
        }

        Self { pool, cache }
    }

    pub async fn get_all(&self) -> Result<Vec<ConnectorStatus>, AppError> {
        let cache_key = "connector_status_all".to_string();
        if let Some(ref c) = self.cache {
            if let Some(cached) = c.get(&cache_key) {
                debug!("Cache hit for connector_status_all");
                return Ok(cached);
            }
        }

        let rows = sqlx::query_as!(
            ConnectorStatus,
            r#"
            SELECT id, name, description
            FROM connector_status
            ORDER BY id
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(AppError::from)?;

        if let Some(ref c) = self.cache {
            c.insert(cache_key.clone(), rows.clone()).await;
            info!("Cached {} connector statuses", rows.len());
        }

        Ok(rows)
    }

    pub async fn insert(&self, cs: &ConnectorStatus) -> Result<(), AppError> {
        sqlx::query!(
            r#"
            INSERT INTO connector_status (name, description)
            VALUES ($1, $2)
            "#,
            cs.name,
            cs.description
        )
        .execute(&self.pool)
        .await
        .map_err(AppError::from)?;

        info!("Inserted new connector status {}", cs.name);

        if let Some(ref c) = self.cache {
            c.invalidate_all().await;
            debug!("ConnectorStatus cache invalidated");
        }

        Ok(())
    }
}
