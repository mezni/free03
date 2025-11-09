use serde::{Deserialize, Serialize};

use crate::domain::value_objects::{NetworkId, Location};

// Query to get station by ID
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetStationByIdQuery {
    pub station_id: i32,
}

// Query to get station by OSM ID
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetStationByOsmIdQuery {
    pub osm_id: i64,
}

// Query to list stations by network
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListStationsByNetworkQuery {
    pub network_id: NetworkId,
    pub page: Option<u32>,
    pub page_size: Option<u32>,
}

// Query to find stations near location
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct FindStationsNearLocationQuery {
    pub latitude: f64,
    pub longitude: f64,
    pub radius_km: f64,
    pub only_operational: bool,
    pub page: Option<u32>,
    pub page_size: Option<u32>,
}

// Query to list operational stations
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListOperationalStationsQuery {
    pub page: Option<u32>,
    pub page_size: Option<u32>,
}

// Query to check station availability
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CheckStationAvailabilityQuery {
    pub station_id: i32,
    pub day_of_week: i32,
    pub time: chrono::NaiveTime,
}

// Query to get station with connectors
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetStationWithConnectorsQuery {
    pub station_id: i32,
}

// Query results
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationDto {
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
    pub created_at: chrono::DateTime<chrono::Utc>,
    pub updated_at: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationWithDistanceDto {
    pub station: StationDto,
    pub distance_meters: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationAvailabilityDto {
    pub day_of_week: i32,
    pub day_name: String,
    pub open_time: Option<chrono::NaiveTime>,
    pub close_time: Option<chrono::NaiveTime>,
    pub is_24_hours: bool,
    pub is_open: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationWithConnectorsDto {
    pub station: StationDto,
    pub connectors: Vec<crate::application::queries::connector_queries::ConnectorDto>,
    pub availability: Vec<StationAvailabilityDto>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationListResponse {
    pub stations: Vec<StationDto>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationSearchResponse {
    pub stations: Vec<StationWithDistanceDto>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}