use serde::{Deserialize, Serialize};
use utoipa::{ToSchema, IntoParams};

use crate::domain::value_objects::{NetworkId, Location};

// ===== REQUESTS =====

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct CreateStationRequest {
    pub network_id: NetworkId,
    #[schema(example = "Downtown Charging Station")]
    pub name: String,
    #[schema(example = "123 Main Street")]
    pub address: String,
    #[schema(example = "New York")]
    pub city: Option<String>,
    #[schema(example = "NY")]
    pub state: Option<String>,
    #[schema(example = "USA")]
    pub country: Option<String>,
    #[schema(example = "10001")]
    pub postal_code: Option<String>,
    pub location: Location,
    pub tags: Option<std::collections::HashMap<String, String>>,
    #[schema(example = 123456789)]
    pub osm_id: Option<i64>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct UpdateStationRequest {
    #[schema(example = "Updated Station Name")]
    pub name: Option<String>,
    #[schema(example = "456 Oak Street")]
    pub address: Option<String>,
    #[schema(example = "Los Angeles")]
    pub city: Option<String>,
    #[schema(example = "CA")]
    pub state: Option<String>,
    #[schema(example = "USA")]
    pub country: Option<String>,
    #[schema(example = "90001")]
    pub postal_code: Option<String>,
    pub location: Option<Location>,
    pub tags: Option<std::collections::HashMap<String, String>>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct UpdateStationStatusRequest {
    pub is_operational: bool,
}

#[derive(Debug, Deserialize, IntoParams)]
pub struct ListStationsParams {
    pub network_id: Option<i32>,
    #[param(example = 1)]
    pub page: Option<u32>,
    #[param(example = 20)]
    pub page_size: Option<u32>,
}

#[derive(Debug, Deserialize, IntoParams)]
pub struct SearchStationsParams {
    #[param(example = 40.7128)]
    pub latitude: f64,
    #[param(example = -74.0060)]
    pub longitude: f64,
    #[param(example = 10.0)]
    pub radius_km: Option<f64>,
    pub only_operational: Option<bool>,
    #[param(example = 1)]
    pub page: Option<u32>,
    #[param(example = 20)]
    pub page_size: Option<u32>,
}

#[derive(Debug, Deserialize, IntoParams)]
pub struct CheckAvailabilityParams {
    pub day_of_week: i32,
    pub time: chrono::NaiveTime,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct StationAvailabilityRuleRequest {
    pub day_of_week: i32,
    pub open_time: Option<chrono::NaiveTime>,
    pub close_time: Option<chrono::NaiveTime>,
    pub is_24_hours: bool,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct UpdateStationAvailabilityRequest {
    pub availability_rules: Vec<StationAvailabilityRuleRequest>,
}

// ===== RESPONSES =====

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct StationResponse {
    pub station_id: i32,
    pub network_id: i32,
    pub name: String,
    pub address: String,
    pub city: Option<String>,
    pub state: Option<String>,
    pub country: Option<String>,
    pub postal_code: Option<String>,
    pub location: Location,
    pub tags: std::collections::HashMap<String, String>,
    pub osm_id: Option<i64>,
    pub is_operational: bool,
    pub created_at: String,
    pub updated_at: String,
}

impl StationResponse {
    pub fn from_dto(dto: crate::application::queries::station_queries::StationDto) -> Self {
        Self {
            station_id: dto.station_id,
            network_id: dto.network_id,
            name: dto.name,
            address: dto.address,
            city: dto.city,
            state: dto.state,
            country: dto.country,
            postal_code: dto.postal_code,
            location: dto.location,
            tags: dto.tags,
            osm_id: dto.osm_id,
            is_operational: dto.is_operational,
            created_at: dto.created_at.to_rfc3339(),
            updated_at: dto.updated_at.to_rfc3339(),
        }
    }
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct StationWithDistanceResponse {
    pub station: StationResponse,
    pub distance_meters: f64,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct StationListResponse {
    pub stations: Vec<StationResponse>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct StationSearchResponse {
    pub stations: Vec<StationWithDistanceResponse>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}

impl StationSearchResponse {
    pub fn from_dto(dto: crate::application::queries::station_queries::StationSearchResponse) -> Self {
        Self {
            stations: dto.stations.into_iter().map(|station_with_distance| {
                StationWithDistanceResponse {
                    station: StationResponse::from_dto(station_with_distance.station),
                    distance_meters: station_with_distance.distance_meters,
                }
            }).collect(),
            total_count: dto.total_count,
            page: dto.page,
            page_size: dto.page_size,
            total_pages: dto.total_pages,
        }
    }
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct StationAvailabilityResponse {
    pub station_id: i32,
    pub message: String,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct StationAvailabilityCheckResponse {
    pub is_open: bool,
    pub current_status: String,
    pub next_opening_time: Option<String>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct StationWithConnectorsResponse {
    pub station: StationResponse,
    pub connectors: Vec<crate::api::dtos::connectors::ConnectorResponse>,
    pub availability: Vec<StationAvailabilityRuleResponse>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct StationAvailabilityRuleResponse {
    pub day_of_week: i32,
    pub day_name: String,
    pub open_time: Option<String>,
    pub close_time: Option<String>,
    pub is_24_hours: bool,
    pub is_open: bool,
}