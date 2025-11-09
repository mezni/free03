use crate::shared::constants::NetworkType;
use crate::shared::errors::AppError;
use actix_web::{HttpResponse, Result, web};
use uuid::Uuid;

use crate::AppState;
use crate::api::dtos::networks::{
    CreateNetworkRequest, NetworkListResponse, NetworkResponse, UpdateNetworkRequest,
};

#[utoipa::path(
    post,
    path = "/api/v1/networks",
    request_body = CreateNetworkRequest,
    responses(
        (status = 201, description = "Network created successfully", body = NetworkResponse),
        (status = 400, description = "Bad request", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Networks"
)]
pub async fn create_network(
    state: web::Data<AppState>,
    request: web::Json<CreateNetworkRequest>,
) -> Result<HttpResponse, AppError> {
    // In a real application, you would get this from authentication context
    let created_by = Uuid::new_v4(); // TODO: Replace with actual user ID from auth

    let network_type = NetworkType::from_str(&request.network_type)
        .ok_or_else(|| AppError::Validation("Invalid network type".to_string()))?;

    let command = crate::application::commands::networks::CreateNetworkCommand {
        name: request.name.clone(),
        network_type,
        contact_email: request.contact_email.clone(),
        phone_number: request.phone_number.clone(),
        address: request.address.clone(),
        created_by,
    };

    let handler = &state.network_command_handler;
    let network = handler.handle_create(command).await?;

    let response = NetworkResponse::from(network);
    Ok(HttpResponse::Created().json(response))
}

#[utoipa::path(
    get,
    path = "/api/v1/networks/{id}",
    params(
        ("id" = i32, Path, description = "Network ID")
    ),
    responses(
        (status = 200, description = "Network found", body = NetworkResponse),
        (status = 404, description = "Network not found", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Networks"
)]
pub async fn get_network(
    state: web::Data<AppState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, AppError> {
    let network_id = path.into_inner();

    let query = crate::application::queries::networks::GetNetworkQuery { network_id };
    let handler = &state.network_query_handler;
    let response = handler.handle_get(query).await?;

    let network_response = NetworkResponse::from(response.network);
    Ok(HttpResponse::Ok().json(network_response))
}

#[utoipa::path(
    get,
    path = "/api/v1/networks",
    params(
        ListNetworksParams
    ),
    responses(
        (status = 200, description = "List of networks", body = NetworkListResponse),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Networks"
)]
pub async fn list_networks(
    state: web::Data<AppState>,
    web::Query(params): web::Query<ListNetworksParams>,
) -> Result<HttpResponse, AppError> {
    let page = params.page.unwrap_or(1);
    let page_size = params
        .page_size
        .unwrap_or(crate::shared::constants::DEFAULT_PAGE_SIZE)
        .min(crate::shared::constants::MAX_PAGE_SIZE);

    let query = crate::application::queries::networks::ListNetworksQuery { page, page_size };
    let handler = &state.network_query_handler;
    let response = handler.handle_list(query).await?;

    let list_response = NetworkListResponse::from(response);
    Ok(HttpResponse::Ok().json(list_response))
}

#[utoipa::path(
    put,
    path = "/api/v1/networks/{id}",
    params(
        ("id" = i32, Path, description = "Network ID")
    ),
    request_body = UpdateNetworkRequest,
    responses(
        (status = 200, description = "Network updated successfully", body = NetworkResponse),
        (status = 400, description = "Bad request", body = AppError),
        (status = 404, description = "Network not found", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Networks"
)]
pub async fn update_network(
    state: web::Data<AppState>,
    path: web::Path<i32>,
    request: web::Json<UpdateNetworkRequest>,
) -> Result<HttpResponse, AppError> {
    let network_id = path.into_inner();

    // In a real application, you would get this from authentication context
    let updated_by = Uuid::new_v4(); // TODO: Replace with actual user ID from auth

    let command = crate::application::commands::networks::UpdateNetworkCommand {
        network_id,
        name: request.name.clone(),
        contact_email: request.contact_email.clone(),
        phone_number: request.phone_number.clone(),
        address: request.address.clone(),
        updated_by,
    };

    let handler = &state.network_command_handler;
    let network = handler.handle_update(command).await?;

    let response = NetworkResponse::from(network);
    Ok(HttpResponse::Ok().json(response))
}

#[utoipa::path(
    delete,
    path = "/api/v1/networks/{id}",
    params(
        ("id" = i32, Path, description = "Network ID")
    ),
    responses(
        (status = 204, description = "Network deleted successfully"),
        (status = 404, description = "Network not found", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Networks"
)]
pub async fn delete_network(
    state: web::Data<AppState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, AppError> {
    let network_id = path.into_inner();

    let command = crate::application::commands::networks::DeleteNetworkCommand { network_id };
    let handler = &state.network_command_handler;
    handler.handle_delete(command).await?;

    Ok(HttpResponse::NoContent().finish())
}

#[derive(serde::Deserialize, utoipa::IntoParams)]
pub struct ListNetworksParams {
    #[param(example = 1)]
    pub page: Option<u32>,

    #[param(example = 20)]
    pub page_size: Option<u32>,
}
