use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Company {
    pub company_id: i32,
    pub network_id: i32,
    pub business_registration_number: Option<String>,
    pub website_url: Option<String>,
    pub created_by: Uuid,
    pub updated_by: Option<Uuid>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl Company {
    pub fn new(
        network_id: i32,
        business_registration_number: Option<String>,
        website_url: Option<String>,
        created_by: Uuid,
    ) -> Result<Self, String> {
        // Validate business registration number if provided
        if let Some(reg_number) = &business_registration_number {
            if reg_number.len() > crate::shared::constants::MAX_BUSINESS_REG_NUMBER_LENGTH {
                // Fixed import
                return Err(format!(
                    "Business registration number cannot exceed {} characters",
                    crate::shared::constants::MAX_BUSINESS_REG_NUMBER_LENGTH // Fixed import
                ));
            }
        }

        // Validate website URL if provided
        if let Some(website) = &website_url {
            if website.len() > crate::shared::constants::MAX_WEBSITE_URL_LENGTH {
                // Fixed import
                return Err(format!(
                    "Website URL cannot exceed {} characters",
                    crate::shared::constants::MAX_WEBSITE_URL_LENGTH // Fixed import
                ));
            }
        }

        Ok(Self {
            company_id: 0,
            network_id,
            business_registration_number,
            website_url,
            created_by,
            updated_by: None,
            created_at: Utc::now(),
            updated_at: Utc::now(),
        })
    }

    pub fn update(
        &mut self,
        business_registration_number: Option<String>,
        website_url: Option<String>,
        updated_by: Uuid,
    ) -> Result<(), String> {
        if let Some(reg_number) = &business_registration_number {
            if reg_number.len() > crate::shared::constants::MAX_BUSINESS_REG_NUMBER_LENGTH {
                // Fixed import
                return Err(format!(
                    "Business registration number cannot exceed {} characters",
                    crate::shared::constants::MAX_BUSINESS_REG_NUMBER_LENGTH // Fixed import
                ));
            }
            self.business_registration_number = Some(reg_number.clone());
        } else {
            self.business_registration_number = None;
        }

        if let Some(website) = &website_url {
            if website.len() > crate::shared::constants::MAX_WEBSITE_URL_LENGTH {
                // Fixed import
                return Err(format!(
                    "Website URL cannot exceed {} characters",
                    crate::shared::constants::MAX_WEBSITE_URL_LENGTH // Fixed import
                ));
            }
            self.website_url = Some(website.clone());
        } else {
            self.website_url = None;
        }

        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();

        Ok(())
    }
}
