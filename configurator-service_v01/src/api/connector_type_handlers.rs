use actix_web::{web, HttpResponse};
use utoipa::IntoParams;
use crate::shared::errors::AppError;
use crate::domain::connector_type_model::ConnectorTypeId;
use crate::application::connector_type_dto::{ConnectorTypeDto, CreateConnectorTypeDto, UpdateConnectorTypeDto};
use crate::application::commands::connector_type_commands::{
    CreateConnectorTypeCommand, UpdateConnectorTypeCommand, DeleteConnectorTypeCommand
};
use crate::application::queries::connector_type_queries::{
    GetConnectorTypeByIdQuery, ListConnectorTypesQuery
};

#[derive(IntoParams)]
pub struct ConnectorTypeIdParam {
    pub id: i32,
}

/// List all connector types
#[utoipa::path(
    get,
    path = "/api/v1/connector-types",
    tag = "connector-types",
    responses(
        (status = 200, description = "List of connector types", body = [ConnectorTypeDto]),
        (status = 500, description = "Internal server error", body = AppError)
    )
)]
pub async fn list_connector_types(
    query: web::Data<ListConnectorTypesQuery<crate::infrastructure::ConnectorTypeRepositoryImpl>>,
) -> HttpResponse {
    match query.execute().await {
        Ok(connector_types) => {
            let dtos: Vec<ConnectorTypeDto> = connector_types.into_iter().map(Into::into).collect();
            HttpResponse::Ok().json(dtos)
        }
        Err(e) => map_error_to_response(e),
    }
}

/// Get connector type by ID
#[utoipa::path(
    get,
    path = "/api/v1/connector-types/{id}",
    tag = "connector-types",
    params(ConnectorTypeIdParam),
    responses(
        (status = 200, description = "Connector type found", body = ConnectorTypeDto),
        (status = 404, description = "Connector type not found"),
        (status = 500, description = "Internal server error", body = AppError)
    )
)]
pub async fn get_connector_type(
    path: web::Path<i32>,
    query: web::Data<GetConnectorTypeByIdQuery<crate::infrastructure::ConnectorTypeRepositoryImpl>>,
) -> HttpResponse {
    let id = ConnectorTypeId::new(path.into_inner());
    
    match query.execute(id).await {
        Ok(Some(connector_type)) => HttpResponse::Ok().json(ConnectorTypeDto::from(connector_type)),
        Ok(None) => HttpResponse::NotFound().body("Connector type not found"),
        Err(e) => map_error_to_response(e),
    }
}

/// Create a new connector type
#[utoipa::path(
    post,
    path = "/api/v1/connector-types",
    tag = "connector-types",
    request_body = CreateConnectorTypeDto,
    responses(
        (status = 201, description = "Connector type created", body = ConnectorTypeDto),
        (status = 400, description = "Validation error", body = AppError),
        (status = 500, description = "Internal server error", body = AppError)
    )
)]
pub async fn create_connector_type(
    command: web::Data<CreateConnectorTypeCommand<crate::infrastructure::ConnectorTypeRepositoryImpl>>,
    dto: web::Json<CreateConnectorTypeDto>,
) -> HttpResponse {
    match command.execute(dto.into_inner()).await {
        Ok(connector_type) => HttpResponse::Created().json(ConnectorTypeDto::from(connector_type)),
        Err(e) => map_error_to_response(e),
    }
}

/// Update an existing connector type
#[utoipa::path(
    put,
    path = "/api/v1/connector-types/{id}",
    tag = "connector-types",
    params(ConnectorTypeIdParam),
    request_body = UpdateConnectorTypeDto,
    responses(
        (status = 200, description = "Connector type updated", body = ConnectorTypeDto),
        (status = 404, description = "Connector type not found"),
        (status = 500, description = "Internal server error", body = AppError)
    )
)]
pub async fn update_connector_type(
    path: web::Path<i32>,
    command: web::Data<UpdateConnectorTypeCommand<crate::infrastructure::ConnectorTypeRepositoryImpl>>,
    dto: web::Json<UpdateConnectorTypeDto>,
) -> HttpResponse {
    let id = ConnectorTypeId::new(path.into_inner());
    
    match command.execute(id, dto.into_inner()).await {
        Ok(connector_type) => HttpResponse::Ok().json(ConnectorTypeDto::from(connector_type)),
        Err(e) => map_error_to_response(e),
    }
}

/// Delete a connector type
#[utoipa::path(
    delete,
    path = "/api/v1/connector-types/{id}",
    tag = "connector-types",
    params(ConnectorTypeIdParam),
    responses(
        (status = 204, description = "Connector type deleted"),
        (status = 404, description = "Connector type not found"),
        (status = 500, description = "Internal server error", body = AppError)
    )
)]
pub async fn delete_connector_type(
    path: web::Path<i32>,
    command: web::Data<DeleteConnectorTypeCommand<crate::infrastructure::ConnectorTypeRepositoryImpl>>,
) -> HttpResponse {
    let id = ConnectorTypeId::new(path.into_inner());
    
    match command.execute(id).await {
        Ok(true) => HttpResponse::NoContent().finish(),
        Ok(false) => HttpResponse::NotFound().body("Connector type not found"),
        Err(e) => map_error_to_response(e),
    }
}

fn map_error_to_response(error: AppError) -> HttpResponse {
    match error.error_type {
        crate::shared::errors::ErrorType::Validation => HttpResponse::BadRequest().json(error),
        crate::shared::errors::ErrorType::NotFound => HttpResponse::NotFound().json(error),
        _ => HttpResponse::InternalServerError().json(error),
    }
}