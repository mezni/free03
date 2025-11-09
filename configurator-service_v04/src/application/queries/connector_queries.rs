use serde::{Deserialize, Serialize};

use crate::domain::value_objects::{StationId, ConnectorStatus};

// Query to get connector by ID
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetConnectorByIdQuery {
    pub connector_id: i32,
}

// Query to list connectors by station
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListConnectorsByStationQuery {
    pub station_id: StationId,
}

// Query to list available connectors by station
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListAvailableConnectorsByStationQuery {
    pub station_id: StationId,
}

// Query to list connectors by status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListConnectorsByStatusQuery {
    pub status: ConnectorStatus,
    pub page: Option<u32>,
    pub page_size: Option<u32>,
}

// Query to get connector types
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListConnectorTypesQuery {
    pub page: Option<u32>,
    pub page_size: Option<u32>,
}

// Query to get connector types by current type
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListConnectorTypesByCurrentTypeQuery {
    pub current_type: crate::domain::value_objects::CurrentType,
}

// Query results
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConnectorDto {
    pub connector_id: i32,
    pub station_id: i32,
    pub connector_type: ConnectorTypeDto,
    pub power_level_kw: f64,
    pub status: ConnectorStatus,
    pub max_voltage: Option<i32>,
    pub max_amperage: Option<i32>,
    pub serial_number: Option<String>,
    pub manufacturer: Option<String>,
    pub model: Option<String>,
    pub installation_date: Option<chrono::NaiveDate>,
    pub last_maintenance_date: Option<chrono::NaiveDate>,
    pub created_at: chrono::DateTime<chrono::Utc>,
    pub updated_at: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConnectorTypeDto {
    pub connector_type_id: i32,
    pub name: String,
    pub description: Option<String>,
    pub standard: Option<String>,
    pub current_type: crate::domain::value_objects::CurrentType,
    pub typical_power_kw: Option<f64>,
    pub pin_configuration: Option<String>,
    pub is_public_standard: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConnectorStatusDto {
    pub connector_id: i32,
    pub station_id: i32,
    pub status: ConnectorStatus,
    pub last_updated: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConnectorListResponse {
    pub connectors: Vec<ConnectorDto>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConnectorTypeListResponse {
    pub connector_types: Vec<ConnectorTypeDto>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}