use crate::shared::errors::AppError;
use actix_web::{HttpResponse, Result, web};
use uuid::Uuid;

use crate::AppState;
use crate::api::dtos::stations::{
    CreateStationRequest, StationResponse, StationsResponse, UpdateStationRequest,
};

#[utoipa::path(
    post,
    path = "/api/v1/stations",
    request_body = CreateStationRequest,
    responses(
        (status = 201, description = "Station created successfully", body = StationResponse),
        (status = 400, description = "Bad request", body = AppError),
        (status = 404, description = "Network not found", body = AppError),
        (status = 409, description = "Station with this name already exists in network", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Stations"
)]
pub async fn create_station(
    state: web::Data<AppState>,
    request: web::Json<CreateStationRequest>,
) -> Result<HttpResponse, AppError> {
    // In a real application, you would get this from authentication context
    let created_by = Uuid::new_v4(); // TODO: Replace with actual user ID from auth

    let command = crate::application::commands::stations::CreateStationCommand {
        network_id: request.network_id,
        name: request.name.clone(),
        address: request.address.clone(),
        city: request.city.clone(),
        state: request.state.clone(),
        country: request.country.clone(),
        postal_code: request.postal_code.clone(),
        location: request.location.clone().into(), // Convert PointDto to Point
        tags: request.tags.clone(),
        osm_id: request.osm_id,
        is_operational: request.is_operational,
        created_by,
    };

    let handler = &state.station_command_handler;
    let station = handler.handle_create(command).await?;

    let response = StationResponse::from(station);
    Ok(HttpResponse::Created().json(response))
}

#[utoipa::path(
    get,
    path = "/api/v1/stations/{id}",
    params(
        ("id" = i32, Path, description = "Station ID")
    ),
    responses(
        (status = 200, description = "Station found", body = StationResponse),
        (status = 404, description = "Station not found", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Stations"
)]
pub async fn get_station(
    state: web::Data<AppState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, AppError> {
    let station_id = path.into_inner();

    let query = crate::application::queries::stations::GetStationQuery { station_id };
    let handler = &state.station_query_handler;
    let response = handler.handle_get(query).await?;

    let station_response = StationResponse::from(response.station);
    Ok(HttpResponse::Ok().json(station_response))
}

#[utoipa::path(
    get,
    path = "/api/v1/stations/network/{network_id}",
    params(
        ("network_id" = i32, Path, description = "Network ID"),
        ListStationsParams
    ),
    responses(
        (status = 200, description = "Stations found", body = StationsResponse),
        (status = 400, description = "Bad request", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Stations"
)]
pub async fn get_stations_by_network(
    state: web::Data<AppState>,
    path: web::Path<i32>,
    web::Query(params): web::Query<ListStationsParams>,
) -> Result<HttpResponse, AppError> {
    let network_id = path.into_inner();
    let page = params.page.unwrap_or(1);
    let page_size = params
        .page_size
        .unwrap_or(crate::shared::constants::DEFAULT_PAGE_SIZE)
        .min(crate::shared::constants::MAX_PAGE_SIZE);

    let query = crate::application::queries::stations::GetStationsByNetworkQuery {
        network_id,
        page,
        page_size,
    };
    let handler = &state.station_query_handler;
    let response = handler.handle_get_by_network(query).await?;

    let stations_response = StationsResponse::from(response);
    Ok(HttpResponse::Ok().json(stations_response))
}

#[utoipa::path(
    get,
    path = "/api/v1/stations/network/{network_id}/operational",
    params(
        ("network_id" = i32, Path, description = "Network ID")
    ),
    responses(
        (status = 200, description = "Operational stations found", body = StationsResponse),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Stations"
)]
pub async fn get_operational_stations(
    state: web::Data<AppState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, AppError> {
    let network_id = path.into_inner();

    let query = crate::application::queries::stations::GetOperationalStationsQuery { network_id };
    let handler = &state.station_query_handler;
    let response = handler.handle_get_operational(query).await?;

    let stations_response = StationsResponse::from(response);
    Ok(HttpResponse::Ok().json(stations_response))
}

#[utoipa::path(
    put,
    path = "/api/v1/stations/{id}",
    params(
        ("id" = i32, Path, description = "Station ID")
    ),
    request_body = UpdateStationRequest,
    responses(
        (status = 200, description = "Station updated successfully", body = StationResponse),
        (status = 400, description = "Bad request", body = AppError),
        (status = 404, description = "Station not found", body = AppError),
        (status = 409, description = "Station with this name already exists in network", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Stations"
)]
pub async fn update_station(
    state: web::Data<AppState>,
    path: web::Path<i32>,
    request: web::Json<UpdateStationRequest>,
) -> Result<HttpResponse, AppError> {
    let station_id = path.into_inner();

    // In a real application, you would get this from authentication context
    let updated_by = Uuid::new_v4(); // TODO: Replace with actual user ID from auth

    let command = crate::application::commands::stations::UpdateStationCommand {
        station_id,
        name: request.name.clone(),
        address: request.address.clone(),
        city: request.city.clone(),
        state: request.state.clone(),
        country: request.country.clone(),
        postal_code: request.postal_code.clone(),
        location: request.location.clone().map(Into::into), // Convert Option<PointDto> to Option<Point>
        tags: request.tags.clone(),
        osm_id: request.osm_id,
        is_operational: request.is_operational,
        updated_by,
    };

    let handler = &state.station_command_handler;
    let station = handler.handle_update(command).await?;

    let response = StationResponse::from(station);
    Ok(HttpResponse::Ok().json(response))
}

#[utoipa::path(
    delete,
    path = "/api/v1/stations/{id}",
    params(
        ("id" = i32, Path, description = "Station ID")
    ),
    responses(
        (status = 204, description = "Station deleted successfully"),
        (status = 404, description = "Station not found", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Stations"
)]
pub async fn delete_station(
    state: web::Data<AppState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, AppError> {
    let station_id = path.into_inner();

    let command = crate::application::commands::stations::DeleteStationCommand { station_id };
    let handler = &state.station_command_handler;
    handler.handle_delete(command).await?;

    Ok(HttpResponse::NoContent().finish())
}

#[utoipa::path(
    get,
    path = "/api/v1/stations/search",
    params(
        SearchStationsParams
    ),
    responses(
        (status = 200, description = "Stations found", body = StationsResponse),
        (status = 400, description = "Bad request", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Stations"
)]
pub async fn search_stations(
    state: web::Data<AppState>,
    web::Query(params): web::Query<SearchStationsParams>,
) -> Result<HttpResponse, AppError> {
    let page = params.page.unwrap_or(1);
    let page_size = params
        .page_size
        .unwrap_or(crate::shared::constants::DEFAULT_PAGE_SIZE)
        .min(crate::shared::constants::MAX_PAGE_SIZE);

    let query = crate::application::queries::stations::SearchStationsQuery {
        network_id: params.network_id,
        name: params.name.clone(),
        city: params.city.clone(),
        country: params.country.clone(),
        is_operational: params.is_operational,
        page,
        page_size,
    };
    let handler = &state.station_query_handler;
    let response = handler.handle_search(query).await?;

    let stations_response = StationsResponse::from(response);
    Ok(HttpResponse::Ok().json(stations_response))
}

#[derive(serde::Deserialize, utoipa::IntoParams)]
pub struct ListStationsParams {
    #[param(example = 1)]
    pub page: Option<u32>,

    #[param(example = 20)]
    pub page_size: Option<u32>,
}

#[derive(serde::Deserialize, utoipa::IntoParams)]
pub struct SearchStationsParams {
    pub network_id: Option<i32>,
    pub name: Option<String>,
    pub city: Option<String>,
    pub country: Option<String>,
    pub is_operational: Option<bool>,

    #[param(example = 1)]
    pub page: Option<u32>,

    #[param(example = 20)]
    pub page_size: Option<u32>,
}
