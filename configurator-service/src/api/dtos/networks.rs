use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};
use utoipa::ToSchema; // Add this import
use uuid::Uuid;

#[derive(Debug, Deserialize, ToSchema)] // Add ToSchema
pub struct CreateNetworkRequest {
    pub name: String,
    pub network_type: String,
    pub contact_email: Option<String>,
    pub phone_number: Option<String>,
    pub address: Option<String>,
}

#[derive(Debug, Deserialize, ToSchema)] // Add ToSchema
pub struct UpdateNetworkRequest {
    pub name: Option<String>,
    pub contact_email: Option<String>,
    pub phone_number: Option<String>,
    pub address: Option<String>,
}

#[derive(Debug, Serialize, ToSchema)] // Add ToSchema
pub struct NetworkResponse {
    pub network_id: i32,
    pub name: String,
    pub network_type: String,
    pub contact_email: Option<String>,
    pub phone_number: Option<String>,
    pub address: Option<String>,
    pub created_by: Uuid,
    pub updated_by: Option<Uuid>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

#[derive(Debug, Serialize, ToSchema)] // Add ToSchema
pub struct NetworkListResponse {
    pub networks: Vec<NetworkResponse>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
}

impl From<crate::domain::entities::networks::Network> for NetworkResponse {
    fn from(network: crate::domain::entities::networks::Network) -> Self {
        Self {
            network_id: network.network_id,
            name: network.name,
            network_type: network.network_type.as_str().to_string(),
            contact_email: network.contact_email,
            phone_number: network.phone_number,
            address: network.address,
            created_by: network.created_by,
            updated_by: network.updated_by,
            created_at: network.created_at,
            updated_at: network.updated_at,
        }
    }
}

impl From<crate::application::queries::networks::NetworkListResponse> for NetworkListResponse {
    fn from(response: crate::application::queries::networks::NetworkListResponse) -> Self {
        Self {
            networks: response
                .networks
                .into_iter()
                .map(NetworkResponse::from)
                .collect(),
            total_count: response.total_count,
            page: response.page,
            page_size: response.page_size,
        }
    }
}
