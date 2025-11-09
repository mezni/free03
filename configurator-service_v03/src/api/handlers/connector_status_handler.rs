use actix_web::{get, post, web, HttpResponse, Responder};
use std::sync::Arc;
use crate::{
    application::commands::connector_status_commands::CreateConnectorStatusCommand,
    application::queries::connector_status_queries::GetConnectorStatusesQuery,
    infrastructure::repositories::connector_status_repo::ConnectorStatusRepository,
    infrastructure::database::DbPool,
    shared::errors::AppError,
};
use crate::api::dtos::connector_status_dto::{ConnectorStatusDTO, CreateConnectorStatusDTO};

/// Get all connector statuses
#[get("/")]
pub async fn get_all_connector_status(db: web::Data<DbPool>) -> impl Responder {
    let repo = ConnectorStatusRepository::new(db.get_ref().clone());
    let query = GetConnectorStatusesQuery::new(repo);

    match query.execute().await {
        Ok(statuses) => HttpResponse::Ok().json(statuses),
        Err(e) => e.error_response(),
    }
}

/// Create a connector status
#[post("/")]
pub async fn create_connector_status(
    db: web::Data<DbPool>,
    payload: web::Json<CreateConnectorStatusDTO>,
) -> impl Responder {
    let repo = ConnectorStatusRepository::new(db.get_ref().clone());
    let command = CreateConnectorStatusCommand::new(repo);

    match command.execute(payload.name.clone(), payload.description.clone()).await {
        Ok(_) => HttpResponse::Created().finish(),
        Err(e) => e.error_response(),
    }
}

/// Configure routes
pub fn configure(cfg: &mut web::ServiceConfig) {
    cfg.service(get_all_connector_status);
    cfg.service(create_connector_status);
}
