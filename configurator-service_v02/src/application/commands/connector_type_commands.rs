use crate::shared::errors::AppError;
use crate::domain::connector_type_model::{ConnectorType, ConnectorTypeId};
use crate::domain::connector_type_repo::ConnectorTypeRepository;
use crate::application::connector_type_dto::{CreateConnectorTypeDto, UpdateConnectorTypeDto};

#[derive(Clone)]
pub struct CreateConnectorTypeCommand<R: ConnectorTypeRepository + Clone> {
    repository: R,
}

impl<R: ConnectorTypeRepository + Clone> CreateConnectorTypeCommand<R> {
    pub fn new(repository: R) -> Self {
        Self { repository }
    }
    
    pub async fn execute(&self, dto: CreateConnectorTypeDto) -> Result<ConnectorType, AppError> {
        if let Some(_) = self.repository.find_by_name(&dto.name).await? {
            return Err(AppError::validation(format!("Connector type '{}' already exists", dto.name)));
        }
        
        let connector_type = ConnectorType::new(
            ConnectorTypeId::new(0),
            dto.name,
            dto.description,
        )?;
        
        self.repository.save(&connector_type).await?;
        Ok(connector_type)
    }
}

#[derive(Clone)]
pub struct UpdateConnectorTypeCommand<R: ConnectorTypeRepository + Clone> {
    repository: R,
}

impl<R: ConnectorTypeRepository + Clone> UpdateConnectorTypeCommand<R> {
    pub fn new(repository: R) -> Self {
        Self { repository }
    }
    
    pub async fn execute(&self, id: ConnectorTypeId, dto: UpdateConnectorTypeDto) -> Result<ConnectorType, AppError> {
        let mut connector_type = self.repository.find_by_id(id).await?
            .ok_or_else(|| AppError::not_found("Connector type not found".to_string()))?;
        
        connector_type.update_description(dto.description);
        self.repository.save(&connector_type).await?;
        
        Ok(connector_type)
    }
}

#[derive(Clone)]
pub struct DeleteConnectorTypeCommand<R: ConnectorTypeRepository + Clone> {
    repository: R,
}

impl<R: ConnectorTypeRepository + Clone> DeleteConnectorTypeCommand<R> {
    pub fn new(repository: R) -> Self {
        Self { repository }
    }
    
    pub async fn execute(&self, id: ConnectorTypeId) -> Result<bool, AppError> {
        if self.repository.find_by_id(id).await?.is_none() {
            return Err(AppError::not_found("Connector type not found".to_string()));
        }
        
        self.repository.delete(id).await
    }
}