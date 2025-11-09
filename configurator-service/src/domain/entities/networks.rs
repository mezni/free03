use crate::shared::constants::NetworkType; // Fixed import
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Network {
    pub network_id: i32,
    pub name: String,
    pub network_type: NetworkType,
    pub contact_email: Option<String>,
    pub phone_number: Option<String>,
    pub address: Option<String>,
    pub created_by: Uuid,
    pub updated_by: Option<Uuid>,
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
        created_by: Uuid,
    ) -> Result<Self, String> {
        // Validate name
        if name.is_empty() {
            return Err("Network name cannot be empty".to_string());
        }
        if name.len() > crate::shared::constants::MAX_NAME_LENGTH {
            // Fixed import
            return Err(format!(
                "Network name cannot exceed {} characters",
                crate::shared::constants::MAX_NAME_LENGTH
            )); // Fixed import
        }

        // Validate email if provided
        if let Some(email) = &contact_email {
            if email.len() > crate::shared::constants::MAX_EMAIL_LENGTH {
                // Fixed import
                return Err(format!(
                    "Email cannot exceed {} characters",
                    crate::shared::constants::MAX_EMAIL_LENGTH
                )); // Fixed import
            }
        }

        // Validate phone number if provided
        if let Some(phone) = &phone_number {
            if phone.len() > crate::shared::constants::MAX_PHONE_LENGTH {
                // Fixed import
                return Err(format!(
                    "Phone number cannot exceed {} characters",
                    crate::shared::constants::MAX_PHONE_LENGTH
                )); // Fixed import
            }
        }

        Ok(Self {
            network_id: 0,
            name,
            network_type,
            contact_email,
            phone_number,
            address,
            created_by,
            updated_by: None,
            created_at: Utc::now(),
            updated_at: Utc::now(),
        })
    }

    pub fn update(
        &mut self,
        name: Option<String>,
        contact_email: Option<String>,
        phone_number: Option<String>,
        address: Option<String>,
        updated_by: Uuid,
    ) -> Result<(), String> {
        if let Some(name) = name {
            if name.is_empty() {
                return Err("Network name cannot be empty".to_string());
            }
            if name.len() > crate::shared::constants::MAX_NAME_LENGTH {
                // Fixed import
                return Err(format!(
                    "Network name cannot exceed {} characters",
                    crate::shared::constants::MAX_NAME_LENGTH
                )); // Fixed import
            }
            self.name = name;
        }

        if let Some(email) = contact_email {
            if email.len() > crate::shared::constants::MAX_EMAIL_LENGTH {
                // Fixed import
                return Err(format!(
                    "Email cannot exceed {} characters",
                    crate::shared::constants::MAX_EMAIL_LENGTH
                )); // Fixed import
            }
            self.contact_email = Some(email);
        } else {
            self.contact_email = None;
        }

        if let Some(phone) = phone_number {
            if phone.len() > crate::shared::constants::MAX_PHONE_LENGTH {
                // Fixed import
                return Err(format!(
                    "Phone number cannot exceed {} characters",
                    crate::shared::constants::MAX_PHONE_LENGTH
                )); // Fixed import
            }
            self.phone_number = Some(phone);
        } else {
            self.phone_number = None;
        }

        self.address = address;
        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();

        Ok(())
    }

    pub fn is_company(&self) -> bool {
        self.network_type == NetworkType::Company
    }

    pub fn is_individual(&self) -> bool {
        self.network_type == NetworkType::Individual
    }
}
