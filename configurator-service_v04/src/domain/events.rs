use serde::{Deserialize, Serialize};
use chrono::{DateTime, Utc};
use super::value_objects::*;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum DomainEvent {
    StationCreated(StationCreated),
    StationStatusChanged(StationStatusChanged),
    ConnectorStatusChanged(ConnectorStatusChanged),
    ChargingSessionStarted(ChargingSessionStarted),
    ChargingSessionCompleted(ChargingSessionCompleted),
    ChargingSessionCancelled(ChargingSessionCancelled),
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationCreated {
    pub station_id: StationId,
    pub network_id: NetworkId,
    pub name: String,
    pub location: Location,
    pub created_by: UserId,
    pub occurred_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationStatusChanged {
    pub station_id: StationId,
    pub is_operational: bool,
    pub changed_by: UserId,
    pub occurred_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ConnectorStatusChanged {
    pub connector_id: ConnectorId,
    pub station_id: StationId,
    pub old_status: ConnectorStatus,
    pub new_status: ConnectorStatus,
    pub changed_by: UserId,
    pub occurred_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChargingSessionStarted {
    pub session_id: ChargingSessionId,
    pub connector_id: ConnectorId,
    pub user_id: UserId,
    pub start_time: DateTime<Utc>,
    pub initiated_by: UserId,
    pub occurred_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChargingSessionCompleted {
    pub session_id: ChargingSessionId,
    pub connector_id: ConnectorId,
    pub user_id: UserId,
    pub energy_delivered_kwh: EnergyKWH,
    pub total_cost: Money,
    pub end_time: DateTime<Utc>,
    pub ended_by: UserId,
    pub occurred_at: DateTime<Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChargingSessionCancelled {
    pub session_id: ChargingSessionId,
    pub connector_id: ConnectorId,
    pub user_id: UserId,
    pub end_time: DateTime<Utc>,
    pub ended_by: UserId,
    pub occurred_at: DateTime<Utc>,
}

// Event trait for domain events
pub trait DomainEventTrait: Send + Sync {
    fn event_type(&self) -> &'static str;
    fn occurred_at(&self) -> DateTime<Utc>;
    fn version(&self) -> i32 {
        1
    }
}

impl DomainEventTrait for DomainEvent {
    fn event_type(&self) -> &'static str {
        match self {
            DomainEvent::StationCreated(_) => "station_created",
            DomainEvent::StationStatusChanged(_) => "station_status_changed",
            DomainEvent::ConnectorStatusChanged(_) => "connector_status_changed",
            DomainEvent::ChargingSessionStarted(_) => "charging_session_started",
            DomainEvent::ChargingSessionCompleted(_) => "charging_session_completed",
            DomainEvent::ChargingSessionCancelled(_) => "charging_session_cancelled",
        }
    }

    fn occurred_at(&self) -> DateTime<Utc> {
        match self {
            DomainEvent::StationCreated(e) => e.occurred_at,
            DomainEvent::StationStatusChanged(e) => e.occurred_at,
            DomainEvent::ConnectorStatusChanged(e) => e.occurred_at,
            DomainEvent::ChargingSessionStarted(e) => e.occurred_at,
            DomainEvent::ChargingSessionCompleted(e) => e.occurred_at,
            DomainEvent::ChargingSessionCancelled(e) => e.occurred_at,
        }
    }
}