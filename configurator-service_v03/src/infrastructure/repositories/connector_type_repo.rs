use crate::domain::connector_type::ConnectorType;
use crate::shared::errors::AppError;
use sqlx::PgPool;
use std::sync::Arc;
use moka::future::Cache;
use tracing::{info, debug};

#[derive(Clone)]
pub struct ConnectorTypeRepository {
    pool: PgPool,
    cache: Option<Arc<Cache<String, Vec<ConnectorType>>>>,
}

impl ConnectorTypeRepository {
    pub fn new(pool: PgPool, cache: Option<Arc<Cache<String, Vec<ConnectorType>>>>) -> Self {
        if let Some(ref c) = cache {
            debug!("ConnectorTypeRepository using shared cache with {} entries", c.entry_count());
        } else {
            debug!("ConnectorTypeRepository initialized without cache");
        }

        Self { pool, cache }
    }

    pub async fn get_all(&self) -> Result<Vec<ConnectorType>, AppError> {
        let cache_key = "connector_types_all".to_string();
        if let Some(ref c) = self.cache {
            if let Some(cached) = c.get(&cache_key) {
                debug!("Cache hit for connector_types_all");
                return Ok(cached);
            }
        }

        let rows = sqlx::query_as!(
            ConnectorType,
            r#"
            SELECT id, name, description
            FROM connector_types
            ORDER BY id
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(AppError::from)?;

        if let Some(ref c) = self.cache {
            c.insert(cache_key.clone(), rows.clone()).await;
            info!("Cached {} connector types", rows.len());
        }

        Ok(rows)
    }

    pub async fn insert(&self, ct: &ConnectorType) -> Result<(), AppError> {
        sqlx::query!(
            r#"
            INSERT INTO connector_types (name, description)
            VALUES ($1, $2)
            "#,
            ct.name,
            ct.description
        )
        .execute(&self.pool)
        .await
        .map_err(AppError::from)?;

        info!("Inserted new connector type {}", ct.name);

        if let Some(ref c) = self.cache {
            c.invalidate_all().await;
            debug!("ConnectorType cache invalidated");
        }

        Ok(())
    }
}
