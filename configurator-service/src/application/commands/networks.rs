use crate::domain::entities::networks::Network;
use crate::domain::repositories::NetworkRepository;
use crate::shared::constants::NetworkType;
use crate::shared::errors::AppError;
use async_trait::async_trait;
use uuid::Uuid;

pub struct CreateNetworkCommand {
    pub name: String,
    pub network_type: NetworkType,
    pub contact_email: Option<String>,
    pub phone_number: Option<String>,
    pub address: Option<String>,
    pub created_by: Uuid,
}

pub struct UpdateNetworkCommand {
    pub network_id: i32,
    pub name: Option<String>,
    pub contact_email: Option<String>,
    pub phone_number: Option<String>,
    pub address: Option<String>,
    pub updated_by: Uuid,
}

pub struct DeleteNetworkCommand {
    pub network_id: i32,
}

#[async_trait]
pub trait NetworkCommandHandler: Send + Sync {
    async fn handle_create(&self, command: CreateNetworkCommand) -> Result<Network, AppError>;
    async fn handle_update(&self, command: UpdateNetworkCommand) -> Result<Network, AppError>;
    async fn handle_delete(&self, command: DeleteNetworkCommand) -> Result<(), AppError>;
}

pub struct NetworkCommandHandlerImpl {
    network_repository: Box<dyn NetworkRepository>,
}

impl NetworkCommandHandlerImpl {
    pub fn new(network_repository: Box<dyn NetworkRepository>) -> Self {
        Self { network_repository }
    }
}

#[async_trait]
impl NetworkCommandHandler for NetworkCommandHandlerImpl {
    async fn handle_create(&self, command: CreateNetworkCommand) -> Result<Network, AppError> {
        // Create new network entity
        let network = Network::new(
            command.name,
            command.network_type,
            command.contact_email,
            command.phone_number,
            command.address,
            command.created_by,
        )?;

        // Save to repository
        let saved_network = self.network_repository.save(&network).await?;

        Ok(saved_network)
    }

    async fn handle_update(&self, command: UpdateNetworkCommand) -> Result<Network, AppError> {
        // Find existing network
        let mut network = self
            .network_repository
            .find_by_id(command.network_id)
            .await?
            .ok_or_else(|| {
                AppError::NotFound(format!("Network with id {} not found", command.network_id))
            })?;

        // Update network entity
        network.update(
            command.name,
            command.contact_email,
            command.phone_number,
            command.address,
            command.updated_by,
        )?;

        // Save updated network
        let updated_network = self.network_repository.save(&network).await?;

        Ok(updated_network)
    }

    async fn handle_delete(&self, command: DeleteNetworkCommand) -> Result<(), AppError> {
        // Check if network exists
        let network = self
            .network_repository
            .find_by_id(command.network_id)
            .await?;

        if network.is_none() {
            return Err(AppError::NotFound(format!(
                "Network with id {} not found",
                command.network_id
            )));
        }

        // Delete network
        self.network_repository.delete(command.network_id).await?;

        Ok(())
    }
}
