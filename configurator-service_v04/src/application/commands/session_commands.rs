use serde::{Deserialize, Serialize};

use crate::domain::value_objects::{ConnectorId, UserId, EnergyKWH, Money};

// Command to start a charging session
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StartChargingSessionCommand {
    pub connector_id: ConnectorId,
    pub user_id: UserId,
    pub payment_method: Option<String>,
}

// Command to complete a charging session
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CompleteChargingSessionCommand {
    pub session_id: i32,
    pub energy_delivered_kwh: EnergyKWH,
    pub total_cost: Money,
    pub ended_by: UserId,
}

// Command to cancel a charging session
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CancelChargingSessionCommand {
    pub session_id: i32,
    pub cancelled_by: UserId,
}

// Command to update session payment status
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UpdateSessionPaymentStatusCommand {
    pub session_id: i32,
    pub payment_status: crate::domain::value_objects::PaymentStatus,
}

// Command to calculate session cost
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CalculateSessionCostCommand {
    pub session_id: i32,
    pub energy_used_kwh: f64,
    pub duration_minutes: i64,
}

// Command to extend charging session
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExtendChargingSessionCommand {
    pub session_id: i32,
    pub additional_minutes: i32,
    pub extended_by: UserId,
}