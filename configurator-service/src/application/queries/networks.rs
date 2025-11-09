use crate::domain::entities::networks::Network; // Fixed import
use crate::domain::repositories::NetworkRepository; // Fixed import
use crate::shared::errors::AppError;
use async_trait::async_trait;

pub struct GetNetworkQuery {
    pub network_id: i32,
}

pub struct ListNetworksQuery {
    pub page: u32,
    pub page_size: u32,
}

pub struct NetworkResponse {
    pub network: Network,
}

pub struct NetworkListResponse {
    pub networks: Vec<Network>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
}

#[async_trait]
pub trait NetworkQueryHandler: Send + Sync {
    async fn handle_get(&self, query: GetNetworkQuery) -> Result<NetworkResponse, AppError>;
    async fn handle_list(&self, query: ListNetworksQuery) -> Result<NetworkListResponse, AppError>;
}

pub struct NetworkQueryHandlerImpl {
    network_repository: Box<dyn NetworkRepository>,
}

impl NetworkQueryHandlerImpl {
    pub fn new(network_repository: Box<dyn NetworkRepository>) -> Self {
        Self { network_repository }
    }
}

#[async_trait]
impl NetworkQueryHandler for NetworkQueryHandlerImpl {
    async fn handle_get(&self, query: GetNetworkQuery) -> Result<NetworkResponse, AppError> {
        let network = self
            .network_repository
            .find_by_id(query.network_id)
            .await?
            .ok_or_else(|| {
                AppError::NotFound(format!("Network with id {} not found", query.network_id))
            })?;

        Ok(NetworkResponse { network })
    }

    async fn handle_list(&self, query: ListNetworksQuery) -> Result<NetworkListResponse, AppError> {
        let page = if query.page == 0 { 1 } else { query.page };
        let page_size = query.page_size.min(crate::shared::constants::MAX_PAGE_SIZE);

        let networks = self.network_repository.find_all(page, page_size).await?;

        // Note: In a real application, you would get the total count from the repository
        // For now, we'll use the length as we don't have pagination metadata
        let total_count = networks.len() as u64;

        Ok(NetworkListResponse {
            networks,
            total_count,
            page,
            page_size,
        })
    }
}
