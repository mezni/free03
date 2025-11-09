use super::super::value_objects::*;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Station {
    pub id: StationId,
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
    pub is_operational: bool,
    pub created_by: UserId,
    pub updated_by: Option<UserId>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl Station {
    pub fn new(
        network_id: NetworkId,
        name: String,
        address: String,
        city: Option<String>,
        state: Option<String>,
        country: Option<String>,
        postal_code: Option<String>,
        location: Location,
        tags: Tags,
        osm_id: Option<OsmId>,
        created_by: UserId,
    ) -> Result<Self, &'static str> {
        if name.trim().is_empty() {
            return Err("Station name cannot be empty");
        }
        if address.trim().is_empty() {
            return Err("Station address cannot be empty");
        }

        let now = Utc::now();
        Ok(Self {
            id: StationId(0), // Will be set by repository
            network_id,
            name,
            address,
            city,
            state,
            country,
            postal_code,
            location,
            tags,
            osm_id,
            is_operational: true,
            created_by,
            updated_by: None,
            created_at: now,
            updated_at: now,
        })
    }

    pub fn update_operational_status(&mut self, is_operational: bool, updated_by: UserId) {
        self.is_operational = is_operational;
        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();
    }

    pub fn update_location(&mut self, location: Location, updated_by: UserId) {
        self.location = location;
        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();
    }

    pub fn add_tag(&mut self, key: String, value: String, updated_by: UserId) {
        self.tags.insert(key, value);
        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();
    }

    pub fn remove_tag(&mut self, key: &str, updated_by: UserId) {
        self.tags.remove(key);
        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();
    }
}