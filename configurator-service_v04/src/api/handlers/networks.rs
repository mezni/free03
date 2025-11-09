use actix_web::{web, HttpResponse};
use utoipa::ToSchema;

use crate::api::ApiState;
use crate::application::services::{ApplicationResult, ApplicationError};
use crate::api::dtos::networks::*;
use crate::api::middleware::authentication::AuthenticatedUser;

#[utoipa::path(
    post,
    path = "/api/v1/networks",
    tag = "networks",
    request_body = CreateNetworkRequest,
    responses(
        (status = 201, description = "Network created successfully", body = NetworkResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn create_network(
    state: web::Data<ApiState>,
    user: AuthenticatedUser,
    payload: web::Json<CreateNetworkRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let command = crate::application::commands::network_commands::CreateNetworkCommand {
        name: payload.name.clone(),
        network_type: payload.network_type,
        contact_email: payload.contact_email.clone(),
        phone_number: payload.phone_number.clone(),
        address: payload.address.clone(),
        created_by: user.user_id,
    };
    
    let network_id = state.app_service.create_network(command).await?;
    
    let network = state.app_service.get_network_by_id(
        crate::application::queries::network_queries::GetNetworkByIdQuery { network_id }
    ).await?;
    
    Ok(HttpResponse::Created().json(NetworkResponse::from_dto(network)))
}

#[utoipa::path(
    get,
    path = "/api/v1/networks/{id}",
    tag = "networks",
    params(
        ("id" = i32, Path, description = "Network ID")
    ),
    responses(
        (status = 200, description = "Network details", body = NetworkResponse),
        (status = 404, description = "Network not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn get_network(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, ApplicationError> {
    let network_id = path.into_inner();
    let network = state.app_service.get_network_by_id(
        crate::application::queries::network_queries::GetNetworkByIdQuery { network_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(NetworkResponse::from_dto(network)))
}

#[utoipa::path(
    get,
    path = "/api/v1/networks",
    tag = "networks",
    params(
        ListNetworksParams
    ),
    responses(
        (status = 200, description = "List of networks", body = NetworkListResponse),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn list_networks(
    state: web::Data<ApiState>,
    query: web::Query<ListNetworksParams>,
) -> Result<HttpResponse, ApplicationError> {
    let query = crate::application::queries::network_queries::ListNetworksQuery {
        page: query.page,
        page_size: query.page_size,
    };
    
    let result = state.app_service.list_networks(query).await?;
    Ok(HttpResponse::Ok().json(NetworkListResponse::from_dto(result)))
}

#[utoipa::path(
    put,
    path = "/api/v1/networks/{id}",
    tag = "networks",
    params(
        ("id" = i32, Path, description = "Network ID")
    ),
    request_body = UpdateNetworkRequest,
    responses(
        (status = 200, description = "Network updated successfully", body = NetworkResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Network not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn update_network(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
    payload: web::Json<UpdateNetworkRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let network_id = path.into_inner();
    let command = crate::application::commands::network_commands::UpdateNetworkCommand {
        network_id,
        name: payload.name.clone(),
        contact_email: payload.contact_email.clone(),
        phone_number: payload.phone_number.clone(),
        address: payload.address.clone(),
        updated_by: user.user_id,
    };
    
    state.app_service.update_network(command).await?;
    
    let network = state.app_service.get_network_by_id(
        crate::application::queries::network_queries::GetNetworkByIdQuery { network_id }
    ).await?;
    
    Ok(HttpResponse::Ok().json(NetworkResponse::from_dto(network)))
}

#[utoipa::path(
    delete,
    path = "/api/v1/networks/{id}",
    tag = "networks",
    params(
        ("id" = i32, Path, description = "Network ID")
    ),
    responses(
        (status = 200, description = "Network deleted successfully", body = DeleteResponse),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Network not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn delete_network(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
) -> Result<HttpResponse, ApplicationError> {
    let network_id = path.into_inner();
    let command = crate::application::commands::network_commands::DeleteNetworkCommand {
        network_id,
        deleted_by: user.user_id,
    };
    
    state.app_service.delete_network(command).await?;
    
    Ok(HttpResponse::Ok().json(DeleteResponse {
        message: "Network deleted successfully".to_string(),
        id: network_id,
    }))
}

#[utoipa::path(
    post,
    path = "/api/v1/networks/{id}/company",
    tag = "networks",
    params(
        ("id" = i32, Path, description = "Network ID")
    ),
    request_body = CreateCompanyRequest,
    responses(
        (status = 201, description = "Company created successfully", body = CompanyResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Network not found"),
        (status = 409, description = "Company already exists for network"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn create_company(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
    payload: web::Json<CreateCompanyRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let network_id = path.into_inner();
    let command = crate::application::commands::network_commands::CreateCompanyCommand {
        network_id,
        business_registration_number: payload.business_registration_number.clone(),
        tax_id: payload.tax_id.clone(),
        company_size: payload.company_size,
        website_url: payload.website_url.clone(),
        created_by: user.user_id,
    };
    
    let company_id = state.app_service.create_company(command).await?;
    
    // In a real implementation, fetch the created company
    Ok(HttpResponse::Created().json(CompanyResponse {
        company_id,
        network_id,
        business_registration_number: payload.business_registration_number.clone(),
        tax_id: payload.tax_id.clone(),
        company_size: payload.company_size,
        website_url: payload.website_url.clone(),
        created_at: chrono::Utc::now().to_rfc3339(),
        updated_at: chrono::Utc::now().to_rfc3339(),
    }))
}

#[utoipa::path(
    get,
    path = "/api/v1/networks/{id}/company",
    tag = "networks",
    params(
        ("id" = i32, Path, description = "Network ID")
    ),
    responses(
        (status = 200, description = "Company details", body = CompanyResponse),
        (status = 404, description = "Company not found"),
        (status = 500, description = "Internal server error")
    )
)]
pub async fn get_company(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, ApplicationError> {
    let network_id = path.into_inner();
    
    // Implementation would fetch company by network ID
    // For now, return a placeholder response
    Err(ApplicationError::NotFound("Company not found".to_string()))
}

#[utoipa::path(
    put,
    path = "/api/v1/networks/{id}/company",
    tag = "networks",
    params(
        ("id" = i32, Path, description = "Network ID")
    ),
    request_body = UpdateCompanyRequest,
    responses(
        (status = 200, description = "Company updated successfully", body = CompanyResponse),
        (status = 400, description = "Invalid input"),
        (status = 401, description = "Unauthorized"),
        (status = 404, description = "Company not found"),
        (status = 500, description = "Internal server error")
    ),
    security(
        ("bearer_auth" = [])
    )
)]
pub async fn update_company(
    state: web::Data<ApiState>,
    path: web::Path<i32>,
    user: AuthenticatedUser,
    payload: web::Json<UpdateCompanyRequest>,
) -> Result<HttpResponse, ApplicationError> {
    let network_id = path.into_inner();
    
    // Implementation would update company
    // For now, return a placeholder response
    Ok(HttpResponse::Ok().json(CompanyResponse {
        company_id: 1,
        network_id,
        business_registration_number: payload.business_registration_number.clone(),
        tax_id: payload.tax_id.clone(),
        company_size: payload.company_size,
        website_url: payload.website_url.clone(),
        created_at: chrono::Utc::now().to_rfc3339(),
        updated_at: chrono::Utc::now().to_rfc3339(),
    }))
}