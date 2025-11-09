use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
use crate::shared::constants::MAX_CONNECTOR_TYPE_NAME_LENGTH;
use super::errors::{DomainResult, validation_error};

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize, ToSchema)]
pub struct ConnectorTypeId(pub i32);

impl ConnectorTypeId {
    pub fn new(id: i32) -> Self {
        Self(id)
    }
    
    pub fn value(&self) -> i32 {
        self.0
    }
}

#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct ConnectorType {
    pub id: ConnectorTypeId,
    pub name: String,
    pub description: Option<String>,
}

impl ConnectorType {
    pub fn new(id: ConnectorTypeId, name: String, description: Option<String>) -> DomainResult<Self> {
        if name.is_empty() {
            return Err(validation_error("Connector type name cannot be empty"));
        }
        
        if name.len() > MAX_CONNECTOR_TYPE_NAME_LENGTH {
            return Err(validation_error("Connector type name cannot exceed 50 characters"));
        }
        
        Ok(Self {
            id,
            name,
            description,
        })
    }
    
    pub fn id(&self) -> &ConnectorTypeId {
        &self.id
    }
    
    pub fn name(&self) -> &str {
        &self.name
    }
    
    pub fn description(&self) -> Option<&str> {
        self.description.as_deref()
    }
    
    pub fn update_description(&mut self, description: Option<String>) {
        self.description = description;
    }
    
    pub fn is_fast_charging(&self) -> bool {
        matches!(
            self.name.as_str(),
            "CCS1" | "CCS2" | "CHAdeMO" | "Tesla Supercharger"
        )
    }
}