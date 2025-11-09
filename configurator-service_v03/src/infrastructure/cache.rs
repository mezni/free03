use moka::future::Cache;
use std::sync::Arc;
use crate::shared::constants::{CACHE_DEFAULT_CAPACITY, CACHE_DEFAULT_TTL};
use crate::domain::{Station, ConnectorStatus, ConnectorType};
use std::time::Duration;
use tracing::debug;

/// Centralized caches for the application
#[derive(Clone)]
pub struct AppCaches {
    pub station_cache: Arc<Cache<String, Vec<Station>>>,
    pub connector_status_cache: Arc<Cache<String, Vec<ConnectorStatus>>>,
    pub connector_type_cache: Arc<Cache<String, Vec<ConnectorType>>>,
}

impl AppCaches {
    pub fn new() -> Self {
        let station_cache = Arc::new(
            Cache::builder()
                .max_capacity(CACHE_DEFAULT_CAPACITY)
                .time_to_live(Duration::from_secs(CACHE_DEFAULT_TTL))
                .build()
        );

        let connector_status_cache = Arc::new(
            Cache::builder()
                .max_capacity(CACHE_DEFAULT_CAPACITY)
                .time_to_live(Duration::from_secs(CACHE_DEFAULT_TTL))
                .build()
        );

        let connector_type_cache = Arc::new(
            Cache::builder()
                .max_capacity(CACHE_DEFAULT_CAPACITY)
                .time_to_live(Duration::from_secs(CACHE_DEFAULT_TTL))
                .build()
        );

        debug!(
            "AppCaches initialized with capacity={} TTL={}s",
            CACHE_DEFAULT_CAPACITY, CACHE_DEFAULT_TTL
        );

        Self {
            station_cache,
            connector_status_cache,
            connector_type_cache,
        }
    }
}
