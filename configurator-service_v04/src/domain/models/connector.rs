use super::super::value_objects::*;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Connector {
    pub id: ConnectorId,
    pub station_id: StationId,
    pub connector_type_id: ConnectorTypeId,
    pub power_level_kw: PowerKW,
    pub status: ConnectorStatus,
    pub max_voltage: Option<i32>,
    pub max_amperage: Option<i32>,
    pub serial_number: Option<String>,
    pub manufacturer: Option<String>,
    pub model: Option<String>,
    pub installation_date: Option<chrono::NaiveDate>,
    pub last_maintenance_date: Option<chrono::NaiveDate>,
    pub created_by: UserId,
    pub updated_by: Option<UserId>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl Connector {
    pub fn new(
        station_id: StationId,
        connector_type_id: ConnectorTypeId,
        power_level_kw: PowerKW,
        max_voltage: Option<i32>,
        max_amperage: Option<i32>,
        serial_number: Option<String>,
        manufacturer: Option<String>,
        model: Option<String>,
        installation_date: Option<chrono::NaiveDate>,
        created_by: UserId,
    ) -> Self {
        let now = Utc::now();
        Self {
            id: ConnectorId(0), // Will be set by repository
            station_id,
            connector_type_id,
            power_level_kw,
            status: ConnectorStatus::Available,
            max_voltage,
            max_amperage,
            serial_number,
            manufacturer,
            model,
            installation_date,
            last_maintenance_date: None,
            created_by,
            updated_by: None,
            created_at: now,
            updated_at: now,
        }
    }

    pub fn update_status(&mut self, status: ConnectorStatus, updated_by: UserId) {
        self.status = status;
        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();
    }

    pub fn record_maintenance(&mut self, maintenance_date: chrono::NaiveDate, updated_by: UserId) {
        self.last_maintenance_date = Some(maintenance_date);
        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();
    }

    pub fn is_available(&self) -> bool {
        matches!(self.status, ConnectorStatus::Available)
    }
}