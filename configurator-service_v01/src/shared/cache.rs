use moka::sync::Cache;
use std::time::Duration;

pub type ConnectorTypeCache = Cache<i32, crate::domain::connector_type_model::ConnectorType>;

pub fn create_connector_type_cache(capacity: u64, ttl_seconds: u64) -> ConnectorTypeCache {
    Cache::builder()
        .max_capacity(capacity)
        .time_to_live(Duration::from_secs(ttl_seconds))
        .build()
}