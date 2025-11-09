use crate::domain::entities::{companies::Company, networks::Network, stations::Station};
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

#[async_trait]
pub trait StationRepository: Send + Sync {
    async fn find_by_id(&self, station_id: i32) -> Result<Option<Station>, AppError>;
    async fn find_by_network_id(
        &self,
        network_id: i32,
        page: u32,
        page_size: u32,
    ) -> Result<Vec<Station>, AppError>;
    //    async fn find_nearby(&self, longitude: f64, latitude: f64, radius_meters: f64, page: u32, page_size: u32) -> Result<Vec<Station>, AppError>;
    async fn save(&self, station: &Station) -> Result<Station, AppError>;
    async fn delete(&self, station_id: i32) -> Result<(), AppError>;
    async fn find_operational_by_network(&self, network_id: i32) -> Result<Vec<Station>, AppError>;
}
