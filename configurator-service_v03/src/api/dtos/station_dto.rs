use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct StationDTO {
    pub id: i64,
    pub osm_id: i64,
    pub name: String,
    pub address: Option<String>,
    pub operator: String,
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct CreateStationDTO {
    pub osm_id: i64,
    pub name: String,
    pub address: Option<String>,
    pub operator: String,
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct UpdateStationDTO {
    pub name: Option<String>,
    pub address: Option<String>,
    pub operator: Option<String>,
}
