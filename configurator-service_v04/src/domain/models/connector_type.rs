use super::super::value_objects::*;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConnectorType {
    pub id: ConnectorTypeId,
    pub name: String,
    pub description: Option<String>,
    pub standard: Option<String>,
    pub current_type: CurrentType,
    pub typical_power_kw: Option<PowerKW>,
    pub pin_configuration: Option<String>,
    pub is_public_standard: bool,
    pub created_by: UserId,
    pub updated_by: Option<UserId>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl ConnectorType {
    pub fn new(
        name: String,
        description: Option<String>,
        standard: Option<String>,
        current_type: CurrentType,
        typical_power_kw: Option<PowerKW>,
        pin_configuration: Option<String>,
        is_public_standard: bool,
        created_by: UserId,
    ) -> Result<Self, &'static str> {
        if name.trim().is_empty() {
            return Err("Connector type name cannot be empty");
        }

        let now = Utc::now();
        Ok(Self {
            id: ConnectorTypeId(0), // Will be set by repository
            name,
            description,
            standard,
            current_type,
            typical_power_kw,
            pin_configuration,
            is_public_standard,
            created_by,
            updated_by: None,
            created_at: now,
            updated_at: now,
        })
    }
}