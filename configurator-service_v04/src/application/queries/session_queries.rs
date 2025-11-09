use serde::{Deserialize, Serialize};

use crate::domain::value_objects::{UserId, ConnectorId};

// Query to get session by ID
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetSessionByIdQuery {
    pub session_id: i32,
}

// Query to list sessions by user
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListSessionsByUserQuery {
    pub user_id: UserId,
    pub page: Option<u32>,
    pub page_size: Option<u32>,
}

// Query to list sessions by connector
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListSessionsByConnectorQuery {
    pub connector_id: ConnectorId,
    pub page: Option<u32>,
    pub page_size: Option<u32>,
}

// Query to list active sessions
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListActiveSessionsQuery {
    pub page: Option<u32>,
    pub page_size: Option<u32>,
}

// Query to get session statistics
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetSessionStatisticsQuery {
    pub start_date: chrono::DateTime<chrono::Utc>,
    pub end_date: chrono::DateTime<chrono::Utc>,
}

// Query to get user session history
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetUserSessionHistoryQuery {
    pub user_id: UserId,
    pub limit: Option<i64>,
}

// Query results
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChargingSessionDto {
    pub session_id: i32,
    pub connector: crate::application::queries::connector_queries::ConnectorDto,
    pub user_id: uuid::Uuid,
    pub start_time: chrono::DateTime<chrono::Utc>,
    pub end_time: Option<chrono::DateTime<chrono::Utc>,
    pub energy_delivered_kwh: Option<f64>,
    pub total_cost: Option<f64>,
    pub payment_status: crate::domain::value_objects::PaymentStatus,
    pub payment_method: Option<String>,
    pub session_status: crate::domain::value_objects::ChargingSessionStatus,
    pub duration_minutes: Option<i64>,
    pub created_at: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionStatisticsDto {
    pub total_sessions: u64,
    pub completed_sessions: u64,
    pub active_sessions: u64,
    pub cancelled_sessions: u64,
    pub total_energy_kwh: f64,
    pub total_revenue: f64,
    pub average_session_duration_minutes: f64,
    pub average_energy_per_session_kwh: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SessionListResponse {
    pub sessions: Vec<ChargingSessionDto>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UserSessionSummary {
    pub user_id: uuid::Uuid,
    pub total_sessions: u64,
    pub total_energy_kwh: f64,
    pub total_cost: f64,
    pub average_session_duration_minutes: f64,
}