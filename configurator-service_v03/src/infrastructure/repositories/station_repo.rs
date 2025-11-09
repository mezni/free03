use crate::domain::station::Station;
use crate::shared::errors::AppError;
use sqlx::PgPool;
use std::sync::Arc;
use moka::future::Cache;
use tracing::{info, debug};

#[derive(Clone)]
pub struct StationRepository {
    pool: PgPool,
    cache: Option<Arc<Cache<String, Vec<Station>>>>,
}

impl StationRepository {
    pub fn new(pool: PgPool, cache: Option<Arc<Cache<String, Vec<Station>>>>) -> Self {
        if let Some(ref c) = cache {
            debug!("StationRepository using shared cache with {} entries", c.entry_count());
        } else {
            debug!("StationRepository initialized without cache");
        }

        Self { pool, cache }
    }

    pub async fn get_stations(&self, limit: i64, offset: i64) -> Result<Vec<Station>, AppError> {
        let cache_key = format!("stations_{offset}_{limit}");
        if let Some(ref c) = self.cache {
            if let Some(cached) = c.get(&cache_key) {
                debug!("Cache hit for key: {}", cache_key);
                return Ok(cached);
            }
        }

        debug!("Cache miss for key: {}. Querying database...", cache_key);

        let rows = sqlx::query_as!(
            Station,
            r#"
            SELECT id, osm_id, name, address, operator, created_at, updated_at
            FROM stations
            ORDER BY id
            LIMIT $1 OFFSET $2
            "#,
            limit,
            offset
        )
        .fetch_all(&self.pool)
        .await
        .map_err(AppError::from)?;

        if let Some(ref c) = self.cache {
            c.insert(cache_key.clone(), rows.clone()).await;
            info!("Cached {} station records for key: {}", rows.len(), cache_key);
        }

        Ok(rows)
    }

    pub async fn insert(&self, station: &Station) -> Result<(), AppError> {
        sqlx::query!(
            r#"
            INSERT INTO stations (osm_id, name, address, operator, created_at, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            "#,
            station.osm_id,
            station.name,
            station.address,
            station.operator,
            station.created_at,
            station.updated_at
        )
        .execute(&self.pool)
        .await
        .map_err(AppError::from)?;

        info!("Inserted new station {}", station.name);

        if let Some(ref c) = self.cache {
            c.invalidate_all().await;
            debug!("Station cache invalidated after insert");
        }

        Ok(())
    }
}
