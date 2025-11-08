use serde::{Deserialize, Serialize};
use utoipa::ToSchema;
use crate::domain::connector_type_model::ConnectorType;

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct ConnectorTypeDto {
    #[schema(value_type = i32)]
    pub id: i32,
    pub name: String,
    pub description: Option<String>,
    pub is_fast_charging: bool,
}

impl From<ConnectorType> for ConnectorTypeDto {
    fn from(connector_type: ConnectorType) -> Self {
        Self {
            id: connector_type.id().value(),
            name: connector_type.name().to_string(),
            description: connector_type.description().map(|s| s.to_string()),
            is_fast_charging: connector_type.is_fast_charging(),
        }
    }
}

#[derive(Debug, Deserialize, ToSchema)]
pub struct CreateConnectorTypeDto {
    pub name: String,
    pub description: Option<String>,
}

#[derive(Debug, Deserialize, ToSchema)]
pub struct UpdateConnectorTypeDto {
    pub description: Option<String>,
}