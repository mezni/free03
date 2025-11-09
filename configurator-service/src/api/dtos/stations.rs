use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use utoipa::ToSchema;
use uuid::Uuid;

// Import the PointDto
use super::points::PointDto;

#[derive(Debug, Deserialize, ToSchema)]
pub struct CreateStationRequest {
    pub network_id: i32,
    pub name: String,
    pub address: String,
    pub city: Option<String>,
    pub state: Option<String>,
    pub country: Option<String>,
    pub postal_code: Option<String>,
    pub location: PointDto, // Use PointDto instead of Point
    pub tags: Option<HashMap<String, String>>,
    pub osm_id: Option<i64>,
    pub is_operational: bool,
}

#[derive(Debug, Deserialize, ToSchema)]
pub struct UpdateStationRequest {
    pub name: Option<String>,
    pub address: Option<String>,
    pub city: Option<String>,
    pub state: Option<String>,
    pub country: Option<String>,
    pub postal_code: Option<String>,
    pub location: Option<PointDto>, // Use PointDto instead of Point
    pub tags: Option<HashMap<String, String>>,
    pub osm_id: Option<i64>,
    pub is_operational: Option<bool>,
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct StationResponse {
    pub station_id: i32,
    pub network_id: i32,
    pub name: String,
    pub address: String,
    pub city: Option<String>,
    pub state: Option<String>,
    pub country: Option<String>,
    pub postal_code: Option<String>,
    pub location: PointDto, // Use PointDto instead of Point
    pub tags: Option<HashMap<String, String>>,
    pub osm_id: Option<i64>,
    pub is_operational: bool,
    pub created_by: Uuid,
    pub updated_by: Option<Uuid>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl From<crate::domain::entities::stations::Station> for StationResponse {
    fn from(station: crate::domain::entities::stations::Station) -> Self {
        Self {
            station_id: station.station_id,
            network_id: station.network_id,
            name: station.name,
            address: station.address,
            city: station.city,
            state: station.state,
            country: station.country,
            postal_code: station.postal_code,
            location: PointDto::from(station.location), // Convert Point to PointDto
            tags: station.tags,
            osm_id: station.osm_id,
            is_operational: station.is_operational,
            created_by: station.created_by,
            updated_by: station.updated_by,
            created_at: station.created_at,
            updated_at: station.updated_at,
        }
    }
}

// Add this for paginated responses
#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct StationsResponse {
    pub stations: Vec<StationResponse>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u64,
}

impl StationsResponse {
    pub fn new(
        stations: Vec<StationResponse>,
        total_count: u64,
        page: u32,
        page_size: u32,
    ) -> Self {
        let total_pages = if page_size > 0 {
            (total_count as f64 / page_size as f64).ceil() as u64
        } else {
            0
        };

        Self {
            stations,
            total_count,
            page,
            page_size,
            total_pages,
        }
    }
}

// Add From implementation for query response
impl From<crate::application::queries::stations::StationsResponse> for StationsResponse {
    fn from(response: crate::application::queries::stations::StationsResponse) -> Self {
        Self::new(
            response
                .stations
                .into_iter()
                .map(StationResponse::from)
                .collect(),
            response.total_count,
            response.page,
            response.page_size,
        )
    }
}
