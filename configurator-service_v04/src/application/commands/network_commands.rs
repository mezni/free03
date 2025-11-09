use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::domain::value_objects::{NetworkType, UserId};

// Command to create a new network
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreateNetworkCommand {
    pub name: String,
    pub network_type: NetworkType,
    pub contact_email: Option<String>,
    pub phone_number: Option<String>,
    pub address: Option<String>,
    pub created_by: UserId,
}

// Command to update an existing network
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UpdateNetworkCommand {
    pub network_id: i32,
    pub name: Option<String>,
    pub contact_email: Option<String>,
    pub phone_number: Option<String>,
    pub address: Option<String>,
    pub updated_by: UserId,
}

// Command to delete a network
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeleteNetworkCommand {
    pub network_id: i32,
    pub deleted_by: UserId,
}

// Command to create a company (extends network)
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreateCompanyCommand {
    pub network_id: i32,
    pub business_registration_number: Option<String>,
    pub tax_id: Option<String>,
    pub company_size: Option<crate::domain::value_objects::CompanySize>,
    pub website_url: Option<String>,
    pub created_by: UserId,
}

// Command to update a company
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UpdateCompanyCommand {
    pub company_id: i32,
    pub business_registration_number: Option<String>,
    pub tax_id: Option<String>,
    pub company_size: Option<crate::domain::value_objects::CompanySize>,
    pub website_url: Option<String>,
    pub updated_by: UserId,
}