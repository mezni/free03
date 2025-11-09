use super::super::value_objects::*;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Company {
    pub id: i32,
    pub network_id: NetworkId,
    pub business_registration_number: Option<String>,
    pub tax_id: Option<String>,
    pub company_size: Option<CompanySize>,
    pub website_url: Option<String>,
    pub created_by: UserId,
    pub updated_by: Option<UserId>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl Company {
    pub fn new(
        network_id: NetworkId,
        business_registration_number: Option<String>,
        tax_id: Option<String>,
        company_size: Option<CompanySize>,
        website_url: Option<String>,
        created_by: UserId,
    ) -> Self {
        let now = Utc::now();
        Self {
            id: 0, // Will be set by repository
            network_id,
            business_registration_number,
            tax_id,
            company_size,
            website_url,
            created_by,
            updated_by: None,
            created_at: now,
            updated_at: now,
        }
    }
}