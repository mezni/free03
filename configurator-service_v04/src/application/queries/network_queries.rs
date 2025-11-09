use serde::{Deserialize, Serialize};

use crate::domain::value_objects::NetworkType;

// Query to get network by ID
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetNetworkByIdQuery {
    pub network_id: i32,
}

// Query to get network by name
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetNetworkByNameQuery {
    pub name: String,
}

// Query to list all networks
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListNetworksQuery {
    pub page: Option<u32>,
    pub page_size: Option<u32>,
}

// Query to list networks by type
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListNetworksByTypeQuery {
    pub network_type: NetworkType,
    pub page: Option<u32>,
    pub page_size: Option<u32>,
}

// Query to get company by network ID
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetCompanyByNetworkIdQuery {
    pub network_id: i32,
}

// Query results
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkDto {
    pub network_id: i32,
    pub name: String,
    pub network_type: NetworkType,
    pub contact_email: Option<String>,
    pub phone_number: Option<String>,
    pub address: Option<String>,
    pub created_at: chrono::DateTime<chrono::Utc>,
    pub updated_at: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CompanyDto {
    pub company_id: i32,
    pub network_id: i32,
    pub business_registration_number: Option<String>,
    pub tax_id: Option<String>,
    pub company_size: Option<crate::domain::value_objects::CompanySize>,
    pub website_url: Option<String>,
    pub created_at: chrono::DateTime<chrono::Utc>,
    pub updated_at: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkWithCompanyDto {
    pub network: NetworkDto,
    pub company: Option<CompanyDto>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NetworkListResponse {
    pub networks: Vec<NetworkDto>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}