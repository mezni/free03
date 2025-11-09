use serde::{Deserialize, Serialize};
use utoipa::{ToSchema, IntoParams};

use crate::domain::value_objects::{StationId, ConnectorTypeId, PowerKW, ConnectorStatus, CurrentType};

// ===== REQUESTS =====

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct CreateConnectorRequest {
    pub station_id: StationId,
    pub connector_type_id: ConnectorTypeId,
    pub power_level_kw: PowerKW,
    pub max_voltage: Option<i32>,
    pub max_amperage: Option<i32>,
    #[schema(example = "SN123456789")]
    pub serial_number: Option<String>,
    #[schema(example = "ABB")]
    pub manufacturer: Option<String>,
    #[schema(example = "Terra HP")]
    pub model: Option<String>,
    pub installation_date: Option<chrono::NaiveDate>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct NewConnectorRequest {
    pub connector_type_id: ConnectorTypeId,
    pub power_level_kw: PowerKW,
    pub max_voltage: Option<i32>,
    pub max_amperage: Option<i32>,
    #[schema(example = "SN123456789")]
    pub serial_number: Option<String>,
    #[schema(example = "ABB")]
    pub manufacturer: Option<String>,
    #[schema(example = "Terra HP")]
    pub model: Option<String>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct BulkCreateConnectorsRequest {
    pub station_id: StationId,
    pub connectors: Vec<NewConnectorRequest>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct UpdateConnectorStatusRequest {
    pub status: ConnectorStatus,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct RecordMaintenanceRequest {
    pub maintenance_date: chrono::NaiveDate,
}

#[derive(Debug, Deserialize, IntoParams)]
pub struct ListConnectorTypesParams {
    #[param(example = 1)]
    pub page: Option<u32>,
    #[param(example = 20)]
    pub page_size: Option<u32>,
    pub current_type: Option<CurrentType>,
}

// ===== RESPONSES =====

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct ConnectorResponse {
    pub connector_id: i32,
    pub station_id: i32,
    pub connector_type: ConnectorTypeResponse,
    pub power_level_kw: f64,
    pub status: ConnectorStatus,
    pub max_voltage: Option<i32>,
    pub max_amperage: Option<i32>,
    pub serial_number: Option<String>,
    pub manufacturer: Option<String>,
    pub model: Option<String>,
    pub installation_date: Option<String>,
    pub last_maintenance_date: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

impl ConnectorResponse {
    pub fn from_dto(dto: crate::application::queries::connector_queries::ConnectorDto) -> Self {
        Self {
            connector_id: dto.connector_id,
            station_id: dto.station_id,
            connector_type: ConnectorTypeResponse::from_dto(dto.connector_type),
            power_level_kw: dto.power_level_kw,
            status: dto.status,
            max_voltage: dto.max_voltage,
            max_amperage: dto.max_amperage,
            serial_number: dto.serial_number,
            manufacturer: dto.manufacturer,
            model: dto.model,
            installation_date: dto.installation_date.map(|d| d.to_string()),
            last_maintenance_date: dto.last_maintenance_date.map(|d| d.to_string()),
            created_at: dto.created_at.to_rfc3339(),
            updated_at: dto.updated_at.to_rfc3339(),
        }
    }
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct ConnectorTypeResponse {
    pub connector_type_id: i32,
    pub name: String,
    pub description: Option<String>,
    pub standard: Option<String>,
    pub current_type: CurrentType,
    pub typical_power_kw: Option<f64>,
    pub pin_configuration: Option<String>,
    pub is_public_standard: bool,
}

impl ConnectorTypeResponse {
    pub fn from_dto(dto: crate::application::queries::connector_queries::ConnectorTypeDto) -> Self {
        Self {
            connector_type_id: dto.connector_type_id,
            name: dto.name,
            description: dto.description,
            standard: dto.standard,
            current_type: dto.current_type,
            typical_power_kw: dto.typical_power_kw,
            pin_configuration: dto.pin_configuration,
            is_public_standard: dto.is_public_standard,
        }
    }
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct ConnectorListResponse {
    pub connectors: Vec<ConnectorResponse>,
    pub total_count: u64,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct ConnectorTypeListResponse {
    pub connector_types: Vec<ConnectorTypeResponse>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct BulkCreateConnectorsResponse {
    pub station_id: i32,
    pub connector_ids: Vec<i32>,
    pub message: String,
}