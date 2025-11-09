use crate::shared::errors::AppError;
use actix_web::{HttpResponse, Result, web};
use uuid::Uuid;

use crate::AppState;
use crate::api::dtos::companies::{CompanyResponse, CreateCompanyRequest, UpdateCompanyRequest};

#[utoipa::path(
    post,
    path = "/api/v1/companies",
    request_body = CreateCompanyRequest,
    responses(
        (status = 201, description = "Company created successfully", body = CompanyResponse),
        (status = 400, description = "Bad request", body = AppError),
        (status = 404, description = "Network not found", body = AppError),
        (status = 409, description = "Company already exists for this network", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Companies"
)]
pub async fn create_company(
    state: web::Data<AppState>,
    request: web::Json<CreateCompanyRequest>,
) -> Result<HttpResponse, AppError> {
    // In a real application, you would get this from authentication context
    let created_by = Uuid::new_v4(); // TODO: Replace with actual user ID from auth

    let command = crate::application::commands::companies::CreateCompanyCommand {
        network_id: request.network_id,
        business_registration_number: request.business_registration_number.clone(),
        website_url: request.website_url.clone(),
        created_by,
    };

    let handler = &state.company_command_handler;
    let company = handler.handle_create(command).await?;

    let response = CompanyResponse::from(company);
    Ok(HttpResponse::Created().json(response))
}

#[utoipa::path(
    get,
    path = "/api/v1/companies/{id}",
    params(
        ("id" = i32, Path, description = "Company ID")
    ),
    responses(
        (status = 200, description = "Company found", body = CompanyResponse),
        (status = 404, description = "Company not found", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Companies"
)]
pub async fn get_company(
    state: web::Data<AppState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, AppError> {
    let company_id = path.into_inner();

    let query = crate::application::queries::companies::GetCompanyQuery { company_id };
    let handler = &state.company_query_handler;
    let response = handler.handle_get(query).await?;

    let company_response = CompanyResponse::from(response.company);
    Ok(HttpResponse::Ok().json(company_response))
}

#[utoipa::path(
    get,
    path = "/api/v1/companies/network/{network_id}",
    params(
        ("network_id" = i32, Path, description = "Network ID")
    ),
    responses(
        (status = 200, description = "Company found for network", body = CompanyResponse),
        (status = 404, description = "Company not found for this network", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Companies"
)]
pub async fn get_company_by_network(
    state: web::Data<AppState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, AppError> {
    let network_id = path.into_inner();

    let query = crate::application::queries::companies::GetCompanyByNetworkQuery { network_id };
    let handler = &state.company_query_handler;
    let response = handler.handle_get_by_network(query).await?;

    let company_response = CompanyResponse::from(response.company);
    Ok(HttpResponse::Ok().json(company_response))
}

#[utoipa::path(
    put,
    path = "/api/v1/companies/{id}",
    params(
        ("id" = i32, Path, description = "Company ID")
    ),
    request_body = UpdateCompanyRequest,
    responses(
        (status = 200, description = "Company updated successfully", body = CompanyResponse),
        (status = 400, description = "Bad request", body = AppError),
        (status = 404, description = "Company not found", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Companies"
)]
pub async fn update_company(
    state: web::Data<AppState>,
    path: web::Path<i32>,
    request: web::Json<UpdateCompanyRequest>,
) -> Result<HttpResponse, AppError> {
    let company_id = path.into_inner();

    // In a real application, you would get this from authentication context
    let updated_by = Uuid::new_v4(); // TODO: Replace with actual user ID from auth

    let command = crate::application::commands::companies::UpdateCompanyCommand {
        company_id,
        business_registration_number: request.business_registration_number.clone(),
        website_url: request.website_url.clone(),
        updated_by,
    };

    let handler = &state.company_command_handler;
    let company = handler.handle_update(command).await?;

    let response = CompanyResponse::from(company);
    Ok(HttpResponse::Ok().json(response))
}

#[utoipa::path(
    delete,
    path = "/api/v1/companies/{id}",
    params(
        ("id" = i32, Path, description = "Company ID")
    ),
    responses(
        (status = 204, description = "Company deleted successfully"),
        (status = 404, description = "Company not found", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    ),
    tag = "Companies"
)]
pub async fn delete_company(
    state: web::Data<AppState>,
    path: web::Path<i32>,
) -> Result<HttpResponse, AppError> {
    let company_id = path.into_inner();

    let command = crate::application::commands::companies::DeleteCompanyCommand { company_id };
    let handler = &state.company_command_handler;
    handler.handle_delete(command).await?;

    Ok(HttpResponse::NoContent().finish())
}
