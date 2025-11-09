use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use utoipa::ToSchema; // Add this import
use uuid::Uuid;

#[derive(Debug, Deserialize, ToSchema)] // Add ToSchema
pub struct CreateCompanyRequest {
    pub network_id: i32,
    pub business_registration_number: Option<String>,
    pub website_url: Option<String>,
}

#[derive(Debug, Deserialize, ToSchema)] // Add ToSchema
pub struct UpdateCompanyRequest {
    pub business_registration_number: Option<String>,
    pub website_url: Option<String>,
}

#[derive(Debug, Serialize, ToSchema)] // Add ToSchema
pub struct CompanyResponse {
    pub company_id: i32,
    pub network_id: i32,
    pub business_registration_number: Option<String>,
    pub website_url: Option<String>,
    pub created_by: Uuid,
    pub updated_by: Option<Uuid>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl From<crate::domain::entities::companies::Company> for CompanyResponse {
    fn from(company: crate::domain::entities::companies::Company) -> Self {
        Self {
            company_id: company.company_id,
            network_id: company.network_id,
            business_registration_number: company.business_registration_number,
            website_url: company.website_url,
            created_by: company.created_by,
            updated_by: company.updated_by,
            created_at: company.created_at,
            updated_at: company.updated_at,
        }
    }
}
