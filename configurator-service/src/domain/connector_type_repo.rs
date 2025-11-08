use async_trait::async_trait;
use crate::shared::errors::AppError;
use super::connector_type_model::{ConnectorType, ConnectorTypeId};

#[async_trait]
pub trait ConnectorTypeRepository: Send + Sync {
    async fn find_by_id(&self, id: ConnectorTypeId) -> Result<Option<ConnectorType>, AppError>;
    async fn find_by_name(&self, name: &str) -> Result<Option<ConnectorType>, AppError>;
    async fn list_all(&self) -> Result<Vec<ConnectorType>, AppError>;
    async fn save(&self, connector_type: &ConnectorType) -> Result<(), AppError>;
    async fn delete(&self, id: ConnectorTypeId) -> Result<bool, AppError>;
}