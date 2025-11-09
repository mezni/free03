use serde::{Deserialize, Serialize};

use crate::domain::value_objects::{StationId, ConnectorTypeId, PowerKW, ConnectorStatus, UserId};

// Command to create a new connector
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreateConnectorCommand {
    pub station_id: StationId,
    pub connector_type_id: ConnectorTypeId,
    pub power_level_kw: PowerKW,
    pub max_voltage: Option<i32>,
    pub max_amperage: Option<i32>,
    pub serial_number: Option<String>,
    pub manufacturer: Option<String>,
    pub model: Option<String>,
    pub installation_date: Option<chrono::NaiveDate>,
    pub created_by: UserId,
}

// Command to update connector status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UpdateConnectorStatusCommand {
    pub connector_id: i32,
    pub status: ConnectorStatus,
    pub updated_by: UserId,
}

// Command to record connector maintenance
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RecordConnectorMaintenanceCommand {
    pub connector_id: i32,
    pub maintenance_date: chrono::NaiveDate,
    pub updated_by: UserId,
}

// Command to delete a connector
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeleteConnectorCommand {
    pub connector_id: i32,
    pub deleted_by: UserId,
}

// Command to create multiple connectors at once
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BulkCreateConnectorsCommand {
    pub station_id: StationId,
    pub connectors: Vec<NewConnector>,
    pub created_by: UserId,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NewConnector {
    pub connector_type_id: ConnectorTypeId,
    pub power_level_kw: PowerKW,
    pub max_voltage: Option<i32>,
    pub max_amperage: Option<i32>,
    pub serial_number: Option<String>,
    pub manufacturer: Option<String>,
    pub model: Option<String>,
}