use actix_web::{web, HttpResponse};
use utoipa::ToSchema;

use crate::api::ApiState;
use crate::application::services::{ApplicationResult, ApplicationError};
use crate::api::dtos::connectors::*;
use crate::api::middleware::authentication::AuthenticatedUser;

#[utoipa::path(
    post,
    path = "/api/v1/connectors",
    tag = "connectors",
    request_body = CreateConnectorRequest,
    responses(
        (status = 201, description = "Connector created successfully", body = ConnectorResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Station not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn create_connector(
    state: web::Data<ApiState>,
    user: AuthenticatedUser,
    payload: web::Json<CreateConnectorRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let command = crate::application::commands::connector_commands::CreateConnectorCommand {
        station_id: payload.station_id,
        connector_type_id: payload.connector_type_id,
        power_level_kw: payload.power_level_kw,
        max_voltage: payload.max_voltage,
        max_amperage: payload.max_amperage,
        serial_number: payload.serial_number.clone(),
        manufacturer: payload.manufacturer.clone(),
        model: payload.model.clone(),
        installation_date: payload.installation_date,
        created_by: user.user_id,
    };
    
    let connector_id = state.app_service.create_connector(command).await?;
    
    let connector = state.app_service.get_connector_by_id(
        crate::application::queries::connector_queries::GetConnectorByIdQuery { connector_id }
    ).await?;
    
    Ok(HttpResponse::Created().json(ConnectorResponse::from_dto(connector)))
}

#[utoipa::path(
    post,
    path = "/api/v1/connectors/bulk",
    tag = "connectors",
    request_body = BulkCreateConnectorsRequest,
    responses(
        (status = 201, description = "Connectors created successfully", body = BulkCreateConnectorsResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Station not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn bulk_create_connectors(
    state: web::Data<ApiState>,
    user: AuthenticatedUser,
    payload: web::Json<BulkCreateConnectorsRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let connectors: Vec<crate::application::commands::connector_commands::NewConnector> = payload
        .connectors
        .iter()
        .map(|connector| crate::application::commands::connector_commands::NewConnector {
            connector_type_id: connector.connector_type_id,
            power_level_kw: connector.power_level_kw,
            max_voltage: connector.max_voltage,
            max_amperage: connector.max_amperage,
            serial_number: connector.serial_number.clone(),
            manufacturer: connector.manufacturer.clone(),
            model: connector.model.clone(),
        })
        .collect();
    
    let command = crate::application::commands::connector_commands::BulkCreateConnectorsCommand {
        station_id: payload.station_id,
        connectors,
        created_by: user.user_id,
    };
    
    let connector_ids = state.app_service.bulk_create_connectors(command).await?;
    
    Ok(HttpResponse::Created().json(BulkCreateConnectorsResponse {
        station_id: payload.station_id.0,
        connector_ids,
        message: format!("Successfully created {} connectors", connector_ids.len()),
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/connectors/{id}",
    tag = "connectors",
    params(
        ("id" = i32, Path, description = "Connector ID")
    ),
    responses(
        (status = 200, description = "Connector details", body = ConnectorResponse),
        (status = 404, description = "Connector not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn get_connector(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, ApplicationError> {
    let connector_id = path.into_inner();
    let connector = state.app_service.get_connector_by_id(
        crate::application::queries::connector_queries::GetConnectorByIdQuery { connector_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(ConnectorResponse::from_dto(connector)))
}

#[utoipa::path(
    put,
    path = "/api/v1/connectors/{id}/status",
    tag = "connectors",
    params(
        ("id" = i32, Path, description = "Connector ID")
    ),
    request_body = UpdateConnectorStatusRequest,
    responses(
        (status = 200, description = "Connector status updated successfully", body = ConnectorResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Connector not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn update_connector_status(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
    payload: web::Json<UpdateConnectorStatusRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let connector_id = path.into_inner();
    let command = crate::application::commands::connector_commands::UpdateConnectorStatusCommand {
        connector_id,
        status: payload.status,
        updated_by: user.user_id,
    };
    
    state.app_service.update_connector_status(command).await?;
    
    let connector = state.app_service.get_connector_by_id(
        crate::application::queries::connector_queries::GetConnectorByIdQuery { connector_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(ConnectorResponse::from_dto(connector)))
}

#[utoipa::path(
    put,
    path = "/api/v1/connectors/{id}/maintenance",
    tag = "connectors",
    params(
        ("id" = i32, Path, description = "Connector ID")
    ),
    request_body = RecordMaintenanceRequest,
    responses(
        (status = 200, description = "Maintenance recorded successfully", body = ConnectorResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Connector not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn record_maintenance(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
    payload: web::Json<RecordMaintenanceRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let connector_id = path.into_inner();
    let command = crate::application::commands::connector_commands::RecordConnectorMaintenanceCommand {
        connector_id,
        maintenance_date: payload.maintenance_date,
        updated_by: user.user_id,
    };
    
    state.app_service.record_connector_maintenance(command).await?;
    
    let connector = state.app_service.get_connector_by_id(
        crate::application::queries::connector_queries::GetConnectorByIdQuery { connector_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(ConnectorResponse::from_dto(connector)))
}

#[utoipa::path(
    delete,
    path = "/api/v1/connectors/{id}",
    tag = "connectors",
    params(
        ("id" = i32, Path, description = "Connector ID")
    ),
    responses(
        (status = 200, description = "Connector deleted successfully", body = DeleteResponse),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Connector not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn delete_connector(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
) -> Result<HttpResponse, ApplicationError> {
    let connector_id = path.into_inner();
    let command = crate::application::commands::connector_commands::DeleteConnectorCommand {
        connector_id,
        deleted_by: user.user_id,
    };
    
    state.app_service.delete_connector(command).await?;
    
    Ok(HttpResponse::Ok().json(crate::api::dtos::networks::DeleteResponse {
        message: "Connector deleted successfully".to_string(),
        id: connector_id,
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/connectors/station/{station_id}",
    tag = "connectors",
    params(
        ("station_id" = i32, Path, description = "Station ID")
    ),
    responses(
        (status = 200, description = "List of connectors for station", body = ConnectorListResponse),
        (status = 404, description = "Station not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn list_connectors_by_station(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, ApplicationError> {
    let station_id = path.into_inner();
    let connectors = state.app_service.list_connectors_by_station(
        crate::application::queries::connector_queries::ListConnectorsByStationQuery {
            station_id: crate::domain::value_objects::StationId(station_id)
        }
    ).await?;
    
    let connector_responses: Vec<ConnectorResponse> = connectors
        .into_iter()
        .map(ConnectorResponse::from_dto)
        .collect();
    
    Ok(HttpResponse::Ok().json(ConnectorListResponse {
        connectors: connector_responses,
        total_count: connector_responses.len() as u64,
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/connectors/station/{station_id}/available",
    tag = "connectors",
    params(
        ("station_id" = i32, Path, description = "Station ID")
    ),
    responses(
        (status = 200, description = "List of available connectors for station", body = ConnectorListResponse),
        (status = 404, description = "Station not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn list_available_connectors(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, ApplicationError> {
    let station_id = path.into_inner();
    let connectors = state.app_service.list_available_connectors(
        crate::application::queries::connector_queries::ListAvailableConnectorsByStationQuery {
            station_id: crate::domain::value_objects::StationId(station_id)
        }
    ).await?;
    
    let connector_responses: Vec<ConnectorResponse> = connectors
        .into_iter()
        .map(ConnectorResponse::from_dto)
        .collect();
    
    Ok(HttpResponse::Ok().json(ConnectorListResponse {
        connectors: connector_responses,
        total_count: connector_responses.len() as u64,
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/connectors/types",
    tag = "connectors",
    params(
        ListConnectorTypesParams
    ),
    responses(
        (status = 200, description = "List of connector types", body = ConnectorTypeListResponse),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn list_connector_types(
    state: web::Data<ApiState>,
    query: web::Query<ListConnectorTypesParams>,
) -> Result<HttpResponse, ApplicationError> {
    let connector_types = if let Some(current_type) = query.current_type {
        state.app_service.find_connector_types_by_current_type(
            crate::application::queries::connector_queries::ListConnectorTypesByCurrentTypeQuery {
                current_type
            }
        ).await?
    } else {
        state.app_service.find_all_connector_types().await?
    };
    
    let type_responses: Vec<ConnectorTypeResponse> = connector_types
        .into_iter()
        .map(ConnectorTypeResponse::from_dto)
        .collect();
    
    Ok(HttpResponse::Ok().json(ConnectorTypeListResponse {
        connector_types: type_responses,
        total_count: type_responses.len() as u64,
        page: query.page.unwrap_or(1),
        page_size: query.page_size.unwrap_or(20),
        total_pages: 1, // Simplified for example
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/connectors/types/current/{current_type}",
    tag = "connectors",
    params(
        ("current_type" = String, Path, description = "Current type (AC or DC)")
    ),
    responses(
        (status = 200, description = "List of connector types by current type", body = ConnectorTypeListResponse),
        (status = 400, description = "Invalid current type"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn list_connector_types_by_current(
    state: web::Data<ApiState>,
    path: web::Path<String>,
) -> Result<HttpResponse, ApplicationError> {
    let current_type_str = path.into_inner();
    let current_type = match current_type_str.as_str() {
        "AC" => crate::domain::value_objects::CurrentType::AC,
        "DC" => crate::domain::value_objects::CurrentType::DC,
        _ => return Err(ApplicationError::ValidationError("Invalid current type. Must be 'AC' or 'DC'".to_string())),
    };
    
    let connector_types = state.app_service.find_connector_types_by_current_type(
        crate::application::queries::connector_queries::ListConnectorTypesByCurrentTypeQuery {
            current_type
        }
    ).await?;
    
    let type_responses: Vec<ConnectorTypeResponse> = connector_types
        .into_iter()
        .map(ConnectorTypeResponse::from_dto)
        .collect();
    
    Ok(HttpResponse::Ok().json(ConnectorTypeListResponse {
        connector_types: type_responses,
        total_count: type_responses.len() as u64,
        page: 1,
        page_size: type_responses.len() as u32,
        total_pages: 1,
    }))
}