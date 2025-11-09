use serde::{Deserialize, Serialize};

use crate::domain::value_objects::{NetworkId, Location, OsmId, UserId, Tags};

// Command to create a new station
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreateStationCommand {
    pub network_id: NetworkId,
    pub name: String,
    pub address: String,
    pub city: Option<String>,
    pub state: Option<String>,
    pub country: Option<String>,
    pub postal_code: Option<String>,
    pub location: Location,
    pub tags: Tags,
    pub osm_id: Option<OsmId>,
    pub created_by: UserId,
}

// Command to update a station
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UpdateStationCommand {
    pub station_id: i32,
    pub name: Option<String>,
    pub address: Option<String>,
    pub city: Option<String>,
    pub state: Option<String>,
    pub country: Option<String>,
    pub postal_code: Option<String>,
    pub location: Option<Location>,
    pub tags: Option<Tags>,
    pub updated_by: UserId,
}

// Command to update station operational status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UpdateStationStatusCommand {
    pub station_id: i32,
    pub is_operational: bool,
    pub updated_by: UserId,
}

// Command to delete a station
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeleteStationCommand {
    pub station_id: i32,
    pub deleted_by: UserId,
}

// Command to add/update station availability
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UpdateStationAvailabilityCommand {
    pub station_id: i32,
    pub availability_rules: Vec<StationAvailabilityRule>,
    pub updated_by: UserId,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationAvailabilityRule {
    pub day_of_week: i32, // 0=Sunday, 6=Saturday
    pub open_time: Option<chrono::NaiveTime>,
    pub close_time: Option<chrono::NaiveTime>,
    pub is_24_hours: bool,
}

// Command to add tags to a station
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AddStationTagsCommand {
    pub station_id: i32,
    pub tags: Tags,
    pub updated_by: UserId,
}

// Command to remove tags from a station
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RemoveStationTagsCommand {
    pub station_id: i32,
    pub tag_keys: Vec<String>,
    pub updated_by: UserId,
}