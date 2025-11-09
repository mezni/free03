use std::sync::Arc;
use crate::shared::errors::AppError;
use crate::domain::connector_type_model::{ConnectorType, ConnectorTypeId};
use crate::domain::connector_type_repo::ConnectorTypeRepository;
use crate::shared::cache::ConnectorTypeCache;

#[derive(Clone)]
pub struct GetConnectorTypeByIdQuery<R: ConnectorTypeRepository + Clone> {
    repository: R,
    cache: Arc<ConnectorTypeCache>,
}

impl<R: ConnectorTypeRepository + Clone> GetConnectorTypeByIdQuery<R> {
    pub fn new(repository: R, cache: Arc<ConnectorTypeCache>) -> Self {
        Self { repository, cache }
    }
    
    pub async fn execute(&self, id: ConnectorTypeId) -> Result<Option<ConnectorType>, AppError> {
        // Try to get from cache first
        if let Some(cached) = self.cache.get(&id.value()) {
            return Ok(Some(cached));
        }
        
        // If not in cache, get from database
        let connector_type = self.repository.find_by_id(id).await?;
        
        // Cache the result if found
        if let Some(ref ct) = connector_type {
            self.cache.insert(id.value(), ct.clone());
        }
        
        Ok(connector_type)
    }
}

#[derive(Clone)]
pub struct GetConnectorTypeByNameQuery<R: ConnectorTypeRepository + Clone> {
    repository: R,
}

impl<R: ConnectorTypeRepository + Clone> GetConnectorTypeByNameQuery<R> {
    pub fn new(repository: R) -> Self {
        Self { repository }
    }
    
    pub async fn execute(&self, name: String) -> Result<Option<ConnectorType>, AppError> {
        self.repository.find_by_name(&name).await
    }
}

#[derive(Clone)]
pub struct ListConnectorTypesQuery<R: ConnectorTypeRepository + Clone> {
    repository: R,
}

impl<R: ConnectorTypeRepository + Clone> ListConnectorTypesQuery<R> {
    pub fn new(repository: R) -> Self {
        Self { repository }
    }
    
    pub async fn execute(&self) -> Result<Vec<ConnectorType>, AppError> {
        self.repository.list_all().await
    }
}