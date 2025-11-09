use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Station {
    pub station_id: i32,
    pub network_id: i32,
    pub name: String,
    pub address: String,
    pub city: Option<String>,
    pub state: Option<String>,
    pub country: Option<String>,
    pub postal_code: Option<String>,
    pub location: Point, // Custom type for PostGIS geography
    pub tags: Option<std::collections::HashMap<String, String>>,
    pub osm_id: Option<i64>,
    pub is_operational: bool,
    pub created_by: Uuid,
    pub updated_by: Option<Uuid>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl Station {
    pub fn new(
        network_id: i32,
        name: String,
        address: String,
        city: Option<String>,
        state: Option<String>,
        country: Option<String>,
        postal_code: Option<String>,
        location: Point,
        tags: Option<std::collections::HashMap<String, String>>,
        osm_id: Option<i64>,
        created_by: Uuid,
    ) -> Result<Self, String> {
        // Validate required fields
        if name.is_empty() {
            return Err("Station name cannot be empty".to_string());
        }
        if name.len() > crate::shared::constants::MAX_NAME_LENGTH {
            return Err(format!(
                "Station name cannot exceed {} characters",
                crate::shared::constants::MAX_NAME_LENGTH
            ));
        }
        if address.is_empty() {
            return Err("Station address cannot be empty".to_string());
        }

        Ok(Self {
            station_id: 0,
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
            created_at: Utc::now(),
            updated_at: Utc::now(),
        })
    }

    pub fn update(
        &mut self,
        name: Option<String>,
        address: Option<String>,
        city: Option<String>,
        state: Option<String>,
        country: Option<String>,
        postal_code: Option<String>,
        location: Option<Point>,
        tags: Option<std::collections::HashMap<String, String>>,
        osm_id: Option<i64>,
        is_operational: Option<bool>,
        updated_by: Uuid,
    ) -> Result<(), String> {
        if let Some(name) = name {
            if name.is_empty() {
                return Err("Station name cannot be empty".to_string());
            }
            if name.len() > crate::shared::constants::MAX_NAME_LENGTH {
                return Err(format!(
                    "Station name cannot exceed {} characters",
                    crate::shared::constants::MAX_NAME_LENGTH
                ));
            }
            self.name = name;
        }

        if let Some(address) = address {
            if address.is_empty() {
                return Err("Station address cannot be empty".to_string());
            }
            self.address = address;
        }

        self.city = city;
        self.state = state;
        self.country = country;
        self.postal_code = postal_code;

        if let Some(location) = location {
            self.location = location;
        }

        self.tags = tags;
        self.osm_id = osm_id;

        if let Some(is_operational) = is_operational {
            self.is_operational = is_operational;
        }

        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();

        Ok(())
    }

    pub fn is_operational(&self) -> bool {
        self.is_operational
    }

    pub fn deactivate(&mut self, updated_by: Uuid) {
        self.is_operational = false;
        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();
    }

    pub fn activate(&mut self, updated_by: Uuid) {
        self.is_operational = true;
        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();
    }
}

// Custom Point type for PostGIS geography
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Point {
    pub longitude: f64,
    pub latitude: f64,
}

impl Point {
    pub fn new(longitude: f64, latitude: f64) -> Result<Self, String> {
        if !(-180.0..=180.0).contains(&longitude) {
            return Err("Longitude must be between -180 and 180".to_string());
        }
        if !(-90.0..=90.0).contains(&latitude) {
            return Err("Latitude must be between -90 and 90".to_string());
        }

        Ok(Self {
            longitude,
            latitude,
        })
    }

    pub fn to_wkt(&self) -> String {
        format!("POINT({} {})", self.longitude, self.latitude)
    }
}
