use serde::{Deserialize, Serialize};
use sqlx::prelude::FromRow;

#[derive(Debug, Serialize, Deserialize, FromRow)]
pub struct ChargingStation {
    pub id: i64,
    pub osm_id: i64,
    pub name: String,
    pub address: Option<String>,
    pub latitude: Option<f64>,
    pub longitude: Option<f64>,
    pub operator: Option<String>,
    pub opening_hours: Option<String>,
    pub capacity: Option<String>,
    pub fee: Option<String>,
    pub parking_fee: Option<String>,
    pub access: Option<String>,
    pub created_at: Option<chrono::DateTime<chrono::Utc>>,
    pub updated_at: Option<chrono::DateTime<chrono::Utc>>,
}

#[derive(Debug, Serialize, Deserialize, FromRow)]
pub struct NearbyStation {
    pub id: i64,
    pub name: String,
    pub address: Option<String>,
    pub distance_meters: Option<f64>,
    pub has_available_connectors: Option<bool>,
    pub total_available_connectors: Option<i64>,
    pub max_power_kw: Option<sqlx::types::BigDecimal>,
    pub power_tier: Option<String>,
    pub operator: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct StationConnector {
    pub id: i64,
    pub station_id: i64,
    pub connector_type: String,
    pub status: String,
    pub current_type: String,
    pub power_kw: Option<sqlx::types::BigDecimal>,
    pub voltage: Option<i32>,
    pub amperage: Option<i32>,
    pub count_available: i32,
    pub count_total: i32,
}

#[derive(Debug, Serialize, Deserialize, FromRow)]
pub struct ConnectorType {
    pub id: i32,
    pub name: String,
    pub description: Option<String>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct Statistics {
    pub total_stations: Option<i64>,
    pub total_connectors: Option<i64>,
    pub available_connectors: Option<i64>,
    pub avg_power_kw: Option<sqlx::types::BigDecimal>,
    pub stations_with_available: Option<i64>,
    pub connector_type_breakdown: Option<serde_json::Value>,
}

#[derive(Debug, Deserialize)]
pub struct NearbyQuery {
    pub lat: f64,
    pub lng: f64,
    pub radius: Option<i32>,
    pub limit: Option<i32>,
}

#[derive(Debug, Deserialize)]
pub struct SearchQuery {
    pub query: Option<String>,
    pub connector_type: Option<String>,
    pub min_power: Option<f64>,
    pub has_available: Option<bool>,
    pub limit: Option<i32>,
    pub offset: Option<i32>,
}

#[derive(Debug, Serialize, Deserialize)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub data: Option<T>,
    pub message: Option<String>,
}