use actix_web::{web, HttpResponse};
use utoipa::ToSchema;

use crate::api::ApiState;
use crate::application::services::{ApplicationResult, ApplicationError};
use crate::api::dtos::stations::*;
use crate::api::middleware::authentication::AuthenticatedUser;

#[utoipa::path(
    post,
    path = "/api/v1/stations",
    tag = "stations",
    request_body = CreateStationRequest,
    responses(
        (status = 201, description = "Station created successfully", body = StationResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Network not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn create_station(
    state: web::Data<ApiState>,
    user: AuthenticatedUser,
    payload: web::Json<CreateStationRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let command = crate::application::commands::station_commands::CreateStationCommand {
        network_id: payload.network_id,
        name: payload.name.clone(),
        address: payload.address.clone(),
        city: payload.city.clone(),
        state: payload.state.clone(),
        country: payload.country.clone(),
        postal_code: payload.postal_code.clone(),
        location: payload.location.clone(),
        tags: payload.tags.clone().unwrap_or_default(),
        osm_id: payload.osm_id,
        created_by: user.user_id,
    };
    
    let station_id = state.app_service.create_station(command).await?;
    
    let station = state.app_service.get_station_by_id(
        crate::application::queries::station_queries::GetStationByIdQuery { station_id }
    ).await?;
    
    Ok(HttpResponse::Created().json(StationResponse::from_dto(station)))
}

#[utoipa::path(
    get,
    path = "/api/v1/stations/{id}",
    tag = "stations",
    params(
        ("id" = i32, Path, description = "Station ID")
    ),
    responses(
        (status = 200, description = "Station details", body = StationResponse),
        (status = 404, description = "Station not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn get_station(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, ApplicationError> {
    let station_id = path.into_inner();
    let station = state.app_service.get_station_by_id(
        crate::application::queries::station_queries::GetStationByIdQuery { station_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(StationResponse::from_dto(station)))
}

#[utoipa::path(
    get,
    path = "/api/v1/stations",
    tag = "stations",
    params(
        ListStationsParams
    ),
    responses(
        (status = 200, description = "List of stations", body = StationListResponse),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn list_stations(
    state: web::Data<ApiState>,
    query: web::Query<ListStationsParams>,
) -> Result<HttpResponse, ApplicationError> {
    let stations = if let Some(network_id) = query.network_id {
        state.app_service.find_stations_by_network(
            crate::application::queries::station_queries::ListStationsByNetworkQuery {
                network_id: crate::domain::value_objects::NetworkId(network_id)
            }
        ).await?
    } else {
        state.app_service.find_operational_stations().await?
    };

    // Convert to response format
    let station_responses: Vec<StationResponse> = stations
        .into_iter()
        .map(StationResponse::from_dto)
        .collect();

    Ok(HttpResponse::Ok().json(StationListResponse {
        stations: station_responses,
        total_count: station_responses.len() as u64,
        page: query.page.unwrap_or(1),
        page_size: query.page_size.unwrap_or(20),
        total_pages: 1, // Simplified for example
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/stations/search",
    tag = "stations",
    params(
        SearchStationsParams
    ),
    responses(
        (status = 200, description = "List of stations near location", body = StationSearchResponse),
        (status = 400, description = "Invalid location parameters"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn search_stations(
    state: web::Data<ApiState>,
    query: web::Query<SearchStationsParams>,
) -> Result<HttpResponse, ApplicationError> {
    let search_query = crate::application::queries::station_queries::FindStationsNearLocationQuery {
        latitude: query.latitude,
        longitude: query.longitude,
        radius_km: query.radius_km.unwrap_or(10.0),
        only_operational: query.only_operational.unwrap_or(true),
        page: query.page,
        page_size: query.page_size,
    };
    
    let result = state.app_service.find_stations_near_location(search_query).await?;
    Ok(HttpResponse::Ok().json(StationSearchResponse::from_dto(result)))
}

#[utoipa::path(
    put,
    path = "/api/v1/stations/{id}",
    tag = "stations",
    params(
        ("id" = i32, Path, description = "Station ID")
    ),
    request_body = UpdateStationRequest,
    responses(
        (status = 200, description = "Station updated successfully", body = StationResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Station not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn update_station(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
    payload: web::Json<UpdateStationRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let station_id = path.into_inner();
    let command = crate::application::commands::station_commands::UpdateStationCommand {
        station_id,
        name: payload.name.clone(),
        address: payload.address.clone(),
        city: payload.city.clone(),
        state: payload.state.clone(),
        country: payload.country.clone(),
        postal_code: payload.postal_code.clone(),
        location: payload.location.clone(),
        tags: payload.tags.clone(),
        updated_by: user.user_id,
    };
    
    state.app_service.update_station(command).await?;
    
    let station = state.app_service.get_station_by_id(
        crate::application::queries::station_queries::GetStationByIdQuery { station_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(StationResponse::from_dto(station)))
}

#[utoipa::path(
    put,
    path = "/api/v1/stations/{id}/status",
    tag = "stations",
    params(
        ("id" = i32, Path, description = "Station ID")
    ),
    request_body = UpdateStationStatusRequest,
    responses(
        (status = 200, description = "Station status updated successfully", body = StationResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Station not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn update_station_status(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
    payload: web::Json<UpdateStationStatusRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let station_id = path.into_inner();
    let command = crate::application::commands::station_commands::UpdateStationStatusCommand {
        station_id,
        is_operational: payload.is_operational,
        updated_by: user.user_id,
    };
    
    state.app_service.update_station_status(command).await?;
    
    let station = state.app_service.get_station_by_id(
        crate::application::queries::station_queries::GetStationByIdQuery { station_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(StationResponse::from_dto(station)))
}

#[utoipa::path(
    delete,
    path = "/api/v1/stations/{id}",
    tag = "stations",
    params(
        ("id" = i32, Path, description = "Station ID")
    ),
    responses(
        (status = 200, description = "Station deleted successfully", body = DeleteResponse),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Station not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn delete_station(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
) -> Result<HttpResponse, ApplicationError> {
    let station_id = path.into_inner();
    let command = crate::application::commands::station_commands::DeleteStationCommand {
        station_id,
        deleted_by: user.user_id,
    };
    
    state.app_service.delete_station(command).await?;
    
    Ok(HttpResponse::Ok().json(DeleteResponse {
        message: "Station deleted successfully".to_string(),
        id: station_id,
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/stations/{id}/connectors",
    tag = "stations",
    params(
        ("id" = i32, Path, description = "Station ID")
    ),
    responses(
        (status = 200, description = "Station with connectors", body = StationWithConnectorsResponse),
        (status = 404, description = "Station not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn get_station_with_connectors(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, ApplicationError> {
    let station_id = path.into_inner();
    
    // Get station
    let station = state.app_service.get_station_by_id(
        crate::application::queries::station_queries::GetStationByIdQuery { station_id }
    ).await?;
    
    // Get connectors for station
    let connectors = state.app_service.list_connectors_by_station(
        crate::application::queries::connector_queries::ListConnectorsByStationQuery {
            station_id: crate::domain::value_objects::StationId(station_id)
        }
    ).await?;
    
    // Convert connectors to response format
    let connector_responses: Vec<crate::api::dtos::connectors::ConnectorResponse> = connectors
        .into_iter()
        .map(crate::api::dtos::connectors::ConnectorResponse::from_dto)
        .collect();
    
    // For now, return empty availability
    let availability = Vec::new();
    
    Ok(HttpResponse::Ok().json(StationWithConnectorsResponse {
        station: StationResponse::from_dto(station),
        connectors: connector_responses,
        availability,
    }))
}

#[utoipa::path(
    put,
    path = "/api/v1/stations/{id}/availability",
    tag = "stations",
    params(
        ("id" = i32, Path, description = "Station ID")
    ),
    request_body = UpdateStationAvailabilityRequest,
    responses(
        (status = 200, description = "Station availability updated successfully", body = StationAvailabilityResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Station not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn update_station_availability(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
    payload: web::Json<UpdateStationAvailabilityRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let station_id = path.into_inner();
    
    let availability_rules: Vec<crate::application::commands::station_commands::StationAvailabilityRule> = payload
        .availability_rules
        .iter()
        .map(|rule| crate::application::commands::station_commands::StationAvailabilityRule {
            day_of_week: rule.day_of_week,
            open_time: rule.open_time,
            close_time: rule.close_time,
            is_24_hours: rule.is_24_hours,
        })
        .collect();
    
    let command = crate::application::commands::station_commands::UpdateStationAvailabilityCommand {
        station_id,
        availability_rules,
        updated_by: user.user_id,
    };
    
    state.app_service.update_station_availability(command).await?;
    
    Ok(HttpResponse::Ok().json(StationAvailabilityResponse {
        station_id,
        message: "Station availability updated successfully".to_string(),
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/stations/{id}/availability/check",
    tag = "stations",
    params(
        ("id" = i32, Path, description = "Station ID"),
        CheckAvailabilityParams
    ),
    responses(
        (status = 200, description = "Station availability status", body = StationAvailabilityCheckResponse),
        (status = 404, description = "Station not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn check_station_availability(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    query: web::Query<CheckAvailabilityParams>,
) -> Result<HttpResponse, ApplicationError> {
    let station_id = path.into_inner();
    
    // Implementation would check station availability
    // For now, return a placeholder response
    Ok(HttpResponse::Ok().json(StationAvailabilityCheckResponse {
        is_open: true,
        current_status: "Open".to_string(),
        next_opening_time: None,
    }))
}