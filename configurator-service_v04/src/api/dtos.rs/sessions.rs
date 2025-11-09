use serde::{Deserialize, Serialize};
use utoipa::{ToSchema, IntoParams};

use crate::domain::value_objects::{ConnectorId, UserId, EnergyKWH, Money, PaymentStatus, ChargingSessionStatus};

// ===== REQUESTS =====

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct StartSessionRequest {
    pub connector_id: ConnectorId,
    pub user_id: UserId,
    #[schema(example = "credit_card")]
    pub payment_method: Option<String>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct CompleteSessionRequest {
    pub energy_delivered_kwh: EnergyKWH,
    pub total_cost: Money,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct UpdatePaymentStatusRequest {
    pub payment_status: PaymentStatus,
}

#[derive(Debug, Deserialize, IntoParams)]
pub struct ListSessionsParams {
    pub user_id: Option<UserId>,
    pub connector_id: Option<ConnectorId>,
    #[param(example = 1)]
    pub page: Option<u32>,
    #[param(example = 20)]
    pub page_size: Option<u32>,
}

#[derive(Debug, Deserialize, IntoParams)]
pub struct SessionStatisticsParams {
    pub start_date: chrono::DateTime<chrono::Utc>,
    pub end_date: chrono::DateTime<chrono::Utc>,
}

// ===== RESPONSES =====

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct SessionResponse {
    pub session_id: i32,
    pub connector: crate::api::dtos::connectors::ConnectorResponse,
    pub user_id: uuid::Uuid,
    pub start_time: String,
    pub end_time: Option<String>,
    pub energy_delivered_kwh: Option<f64>,
    pub total_cost: Option<f64>,
    pub payment_status: PaymentStatus,
    pub payment_method: Option<String>,
    pub session_status: ChargingSessionStatus,
    pub duration_minutes: Option<i64>,
    pub created_at: String,
}

impl SessionResponse {
    pub fn from_dto(dto: crate::application::queries::session_queries::ChargingSessionDto) -> Self {
        Self {
            session_id: dto.session_id,
            connector: crate::api::dtos::connectors::ConnectorResponse::from_dto(dto.connector),
            user_id: dto.user_id,
            start_time: dto.start_time.to_rfc3339(),
            end_time: dto.end_time.map(|t| t.to_rfc3339()),
            energy_delivered_kwh: dto.energy_delivered_kwh,
            total_cost: dto.total_cost,
            payment_status: dto.payment_status,
            payment_method: dto.payment_method,
            session_status: dto.session_status,
            duration_minutes: dto.duration_minutes,
            created_at: dto.created_at.to_rfc3339(),
        }
    }
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct SessionListResponse {
    pub sessions: Vec<SessionResponse>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct SessionStatisticsResponse {
    pub total_sessions: u64,
    pub completed_sessions: u64,
    pub active_sessions: u64,
    pub cancelled_sessions: u64,
    pub total_energy_kwh: f64,
    pub total_revenue: f64,
    pub average_session_duration_minutes: f64,
    pub average_energy_per_session_kwh: f64,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct UserSessionHistoryResponse {
    pub user_id: uuid::Uuid,
    pub sessions: Vec<SessionResponse>,
    pub total_sessions: u64,
    pub total_energy_kwh: f64,
    pub total_cost: f64,
}