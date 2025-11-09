use super::super::value_objects::*;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Network {
    pub id: NetworkId,
    pub name: String,
    pub network_type: NetworkType,
    pub contact_email: Option<String>,
    pub phone_number: Option<String>,
    pub address: Option<String>,
    pub created_by: UserId,
    pub updated_by: Option<UserId>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl Network {
    pub fn new(
        name: String,
        network_type: NetworkType,
        contact_email: Option<String>,
        phone_number: Option<String>,
        address: Option<String>,
        created_by: UserId,
    ) -> Result<Self, &'static str> {
        if name.trim().is_empty() {
            return Err("Network name cannot be empty");
        }

        let now = Utc::now();
        Ok(Self {
            id: NetworkId(0), // Will be set by repository
            name,
            network_type,
            contact_email,
            phone_number,
            address,
            created_by,
            updated_by: None,
            created_at: now,
            updated_at: now,
        })
    }

    pub fn update(
        &mut self,
        name: Option<String>,
        contact_email: Option<String>,
        phone_number: Option<String>,
        address: Option<String>,
        updated_by: UserId,
    ) -> Result<(), &'static str> {
        if let Some(name) = name {
            if name.trim().is_empty() {
                return Err("Network name cannot be empty");
            }
            self.name = name;
        }

        self.contact_email = contact_email;
        self.phone_number = phone_number;
        self.address = address;
        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();

        Ok(())
    }
}