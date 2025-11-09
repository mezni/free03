use crate::domain::entities::companies::Company;
use crate::domain::entities::networks::Network;
use crate::shared::errors::AppError;
use async_trait::async_trait;

#[async_trait]
pub trait NetworkRepository: Send + Sync {
    async fn find_by_id(&self, network_id: i32) -> Result<Option<Network>, AppError>;
    async fn save(&self, network: &Network) -> Result<Network, AppError>;
    async fn delete(&self, network_id: i32) -> Result<(), AppError>;
    async fn find_all(&self, page: u32, page_size: u32) -> Result<Vec<Network>, AppError>;
}

#[async_trait]
pub trait CompanyRepository: Send + Sync {
    async fn find_by_id(&self, company_id: i32) -> Result<Option<Company>, AppError>;
    async fn find_by_network_id(&self, network_id: i32) -> Result<Option<Company>, AppError>;
    async fn save(&self, company: &Company) -> Result<Company, AppError>;
    async fn delete(&self, company_id: i32) -> Result<(), AppError>;
}
