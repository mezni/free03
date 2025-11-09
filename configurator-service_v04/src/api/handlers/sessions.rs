use actix_web::{web, HttpResponse};
use utoipa::ToSchema;

use crate::api::ApiState;
use crate::application::services::{ApplicationResult, ApplicationError};
use crate::api::dtos::sessions::*;
use crate::api::middleware::authentication::AuthenticatedUser;

#[utoipa::path(
    post,
    path = "/api/v1/sessions",
    tag = "sessions",
    request_body = StartSessionRequest,
    responses(
        (status = 201, description = "Charging session started successfully", body = SessionResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Connector not found"),
        (status = 409, description = "Connector not available"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn start_session(
    state: web::Data<ApiState>,
    user: AuthenticatedUser,
    payload: web::Json<StartSessionRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let command = crate::application::commands::session_commands::StartChargingSessionCommand {
        connector_id: payload.connector_id,
        user_id: payload.user_id,
        payment_method: payload.payment_method.clone(),
    };
    
    let session_id = state.app_service.start_charging_session(command).await?;
    
    let session = state.app_service.get_session_by_id(
        crate::application::queries::session_queries::GetSessionByIdQuery { session_id }
    ).await?;
    
    Ok(HttpResponse::Created().json(SessionResponse::from_dto(session)))
}

#[utoipa::path(
    get,
    path = "/api/v1/sessions/{id}",
    tag = "sessions",
    params(
        ("id" = i32, Path, description = "Session ID")
    ),
    responses(
        (status = 200, description = "Session details", body = SessionResponse),
        (status = 404, description = "Session not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn get_session(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, ApplicationError> {
    let session_id = path.into_inner();
    let session = state.app_service.get_session_by_id(
        crate::application::queries::session_queries::GetSessionByIdQuery { session_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(SessionResponse::from_dto(session)))
}

#[utoipa::path(
    put,
    path = "/api/v1/sessions/{id}/complete",
    tag = "sessions",
    params(
        ("id" = i32, Path, description = "Session ID")
    ),
    request_body = CompleteSessionRequest,
    responses(
        (status = 200, description = "Session completed successfully", body = SessionResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Session not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn complete_session(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
    payload: web::Json<CompleteSessionRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let session_id = path.into_inner();
    let command = crate::application::commands::session_commands::CompleteChargingSessionCommand {
        session_id,
        energy_delivered_kwh: payload.energy_delivered_kwh,
        total_cost: payload.total_cost,
        ended_by: user.user_id,
    };
    
    state.app_service.complete_charging_session(command).await?;
    
    let session = state.app_service.get_session_by_id(
        crate::application::queries::session_queries::GetSessionByIdQuery { session_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(SessionResponse::from_dto(session)))
}

#[utoipa::path(
    put,
    path = "/api/v1/sessions/{id}/cancel",
    tag = "sessions",
    params(
        ("id" = i32, Path, description = "Session ID")
    ),
    responses(
        (status = 200, description = "Session cancelled successfully", body = SessionResponse),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Session not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn cancel_session(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
) -> Result<HttpResponse, ApplicationError> {
    let session_id = path.into_inner();
    let command = crate::application::commands::session_commands::CancelChargingSessionCommand {
        session_id,
        cancelled_by: user.user_id,
    };
    
    state.app_service.cancel_charging_session(command).await?;
    
    let session = state.app_service.get_session_by_id(
        crate::application::queries::session_queries::GetSessionByIdQuery { session_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(SessionResponse::from_dto(session)))
}

#[utoipa::path(
    put,
    path = "/api/v1/sessions/{id}/payment",
    tag = "sessions",
    params(
        ("id" = i32, Path, description = "Session ID")
    ),
    request_body = UpdatePaymentStatusRequest,
    responses(
        (status = 200, description = "Payment status updated successfully", body = SessionResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Session not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn update_payment_status(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    _user: AuthenticatedUser,
    payload: web::Json<UpdatePaymentStatusRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let session_id = path.into_inner();
    let command = crate::application::commands::session_commands::UpdateSessionPaymentStatusCommand {
        session_id,
        payment_status: payload.payment_status,
    };
    
    state.app_service.update_session_payment_status(command).await?;
    
    let session = state.app_service.get_session_by_id(
        crate::application::queries::session_queries::GetSessionByIdQuery { session_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(SessionResponse::from_dto(session)))
}

#[utoipa::path(
    get,
    path = "/api/v1/sessions/user/{user_id}",
    tag = "sessions",
    params(
        ("user_id" = String, Path, description = "User ID"),
        ListSessionsParams
    ),
    responses(
        (status = 200, description = "List of sessions for user", body = SessionListResponse),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn list_sessions_by_user(
    state: web::Data<ApiState>,
    path: web::Path<String>,
    query: web::Query<ListSessionsParams>,
) -> Result<HttpResponse, ApplicationError> {
    let user_id_str = path.into_inner();
    let user_id = crate::domain::value_objects::UserId::parse_str(&user_id_str)
        .map_err(|_| ApplicationError::ValidationError("Invalid user ID format".to_string()))?;
    
    let sessions = state.app_service.list_sessions_by_user(
        crate::application::queries::session_queries::ListSessionsByUserQuery {
            user_id,
            page: query.page,
            page_size: query.page_size,
        }
    ).await?;
    
    let session_responses: Vec<SessionResponse> = sessions
        .sessions
        .into_iter()
        .map(SessionResponse::from_dto)
        .collect();
    
    Ok(HttpResponse::Ok().json(SessionListResponse {
        sessions: session_responses,
        total_count: sessions.total_count,
        page: sessions.page,
        page_size: sessions.page_size,
        total_pages: sessions.total_pages,
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/sessions/active",
    tag = "sessions",
    params(
        ListSessionsParams
    ),
    responses(
        (status = 200, description = "List of active sessions", body = SessionListResponse),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn list_active_sessions(
    state: web::Data<ApiState>,
    query: web::Query<ListSessionsParams>,
) -> Result<HttpResponse, ApplicationError> {
    let sessions = state.app_service.list_active_sessions(
        crate::application::queries::session_queries::ListActiveSessionsQuery {
            page: query.page,
            page_size: query.page_size,
        }
    ).await?;
    
    let session_responses: Vec<SessionResponse> = sessions
        .sessions
        .into_iter()
        .map(SessionResponse::from_dto)
        .collect();
    
    Ok(HttpResponse::Ok().json(SessionListResponse {
        sessions: session_responses,
        total_count: sessions.total_count,
        page: sessions.page,
        page_size: sessions.page_size,
        total_pages: sessions.total_pages,
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/sessions/statistics",
    tag = "sessions",
    params(
        SessionStatisticsParams
    ),
    responses(
        (status = 200, description = "Session statistics", body = SessionStatisticsResponse),
        (status = 400, description = "Invalid date range"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn get_session_statistics(
    state: web::Data<ApiState>,
    query: web::Query<SessionStatisticsParams>,
) -> Result<HttpResponse, ApplicationError> {
    let statistics = state.app_service.get_session_statistics(
        crate::application::queries::session_queries::GetSessionStatisticsQuery {
            start_date: query.start_date,
            end_date: query.end_date,
        }
    ).await?;
    
    Ok(HttpResponse::Ok().json(SessionStatisticsResponse {
        total_sessions: statistics.total_sessions,
        completed_sessions: statistics.completed_sessions,
        active_sessions: statistics.active_sessions,
        cancelled_sessions: statistics.cancelled_sessions,
        total_energy_kwh: statistics.total_energy_kwh,
        total_revenue: statistics.total_revenue,
        average_session_duration_minutes: statistics.average_session_duration_minutes,
        average_energy_per_session_kwh: statistics.average_energy_per_session_kwh,
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/sessions/user/{user_id}/history",
    tag = "sessions",
    params(
        ("user_id" = String, Path, description = "User ID")
    ),
    responses(
        (status = 200, description = "User session history", body = UserSessionHistoryResponse),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn get_user_session_history(
    state: web::Data<ApiState>,
    path: web::Path<String>,
) -> Result<HttpResponse, ApplicationError> {
    let user_id_str = path.into_inner();
    let user_id = crate::domain::value_objects::UserId::parse_str(&user_id_str)
        .map_err(|_| ApplicationError::ValidationError("Invalid user ID format".to_string()))?;
    
    let sessions = state.app_service.get_user_session_history(
        crate::application::queries::session_queries::GetUserSessionHistoryQuery {
            user_id,
            limit: Some(50), // Default limit
        }
    ).await?;
    
    let session_responses: Vec<SessionResponse> = sessions
        .into_iter()
        .map(SessionResponse::from_dto)
        .collect();
    
    // Calculate totals
    let total_energy_kwh = session_responses.iter()
        .filter_map(|s| s.energy_delivered_kwh)
        .sum();
    
    let total_cost = session_responses.iter()
        .filter_map(|s| s.total_cost)
        .sum();
    
    Ok(HttpResponse::Ok().json(UserSessionHistoryResponse {
        user_id: user_id.0,
        sessions: session_responses,
        total_sessions: session_responses.len() as u64,
        total_energy_kwh,
        total_cost,
    }))
}