use serde::{Deserialize, Serialize};
use utoipa::{ToSchema, IntoParams};

use crate::domain::value_objects::{NetworkType, CompanySize};

// ===== REQUESTS =====

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct CreateNetworkRequest {
    #[schema(example = "EV Charging Network")]
    pub name: String,
    pub network_type: NetworkType,
    #[schema(example = "contact@evnetwork.com")]
    pub contact_email: Option<String>,
    #[schema(example = "+1234567890")]
    pub phone_number: Option<String>,
    #[schema(example = "123 Main St, City, Country")]
    pub address: Option<String>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct UpdateNetworkRequest {
    #[schema(example = "Updated Network Name")]
    pub name: Option<String>,
    #[schema(example = "updated@evnetwork.com")]
    pub contact_email: Option<String>,
    #[schema(example = "+0987654321")]
    pub phone_number: Option<String>,
    #[schema(example = "456 Oak St, City, Country")]
    pub address: Option<String>,
}

#[derive(Debug, Deserialize, IntoParams)]
pub struct ListNetworksParams {
    #[param(example = 1)]
    pub page: Option<u32>,
    #[param(example = 20)]
    pub page_size: Option<u32>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct CreateCompanyRequest {
    #[schema(example = "123456789")]
    pub business_registration_number: Option<String>,
    #[schema(example = "TAX-123-456-789")]
    pub tax_id: Option<String>,
    pub company_size: Option<CompanySize>,
    #[schema(example = "https://evnetwork.com")]
    pub website_url: Option<String>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct UpdateCompanyRequest {
    #[schema(example = "987654321")]
    pub business_registration_number: Option<String>,
    #[schema(example = "TAX-987-654-321")]
    pub tax_id: Option<String>,
    pub company_size: Option<CompanySize>,
    #[schema(example = "https://newevnetwork.com")]
    pub website_url: Option<String>,
}

// ===== RESPONSES =====

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct NetworkResponse {
    pub network_id: i32,
    pub name: String,
    pub network_type: NetworkType,
    pub contact_email: Option<String>,
    pub phone_number: Option<String>,
    pub address: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

impl NetworkResponse {
    pub fn from_dto(dto: crate::application::queries::network_queries::NetworkDto) -> Self {
        Self {
            network_id: dto.network_id,
            name: dto.name,
            network_type: dto.network_type,
            contact_email: dto.contact_email,
            phone_number: dto.phone_number,
            address: dto.address,
            created_at: dto.created_at.to_rfc3339(),
            updated_at: dto.updated_at.to_rfc3339(),
        }
    }
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct NetworkListResponse {
    pub networks: Vec<NetworkResponse>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}

impl NetworkListResponse {
    pub fn from_dto(dto: crate::application::queries::network_queries::NetworkListResponse) -> Self {
        Self {
            networks: dto.networks.into_iter().map(NetworkResponse::from_dto).collect(),
            total_count: dto.total_count,
            page: dto.page,
            page_size: dto.page_size,
            total_pages: dto.total_pages,
        }
    }
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct CompanyResponse {
    pub company_id: i32,
    pub network_id: i32,
    pub business_registration_number: Option<String>,
    pub tax_id: Option<String>,
    pub company_size: Option<CompanySize>,
    pub website_url: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

// ===== COMMON =====

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct DeleteResponse {
    pub message: String,
    pub id: i32,
}