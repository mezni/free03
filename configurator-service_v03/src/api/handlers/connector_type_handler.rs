use actix_web::{get, post, web, HttpResponse, Responder};
use crate::{
    application::commands::connector_type_commands::CreateConnectorTypeCommand,
    application::queries::connector_type_queries::GetConnectorTypesQuery,
    infrastructure::repositories::connector_type_repo::ConnectorTypeRepository,
    infrastructure::database::DbPool,
    shared::errors::AppError,
};
use crate::api::dtos::connector_type_dto::{ConnectorTypeDTO, CreateConnectorTypeDTO};

#[get("/")]
pub async fn get_all_connector_types(db: web::Data<DbPool>) -> impl Responder {
    let repo = ConnectorTypeRepository::new(db.get_ref().clone());
    let query = GetConnectorTypesQuery::new(repo);

    match query.execute().await {
        Ok(types) => HttpResponse::Ok().json(types),
        Err(e) => e.error_response(),
    }
}

#[post("/")]
pub async fn create_connector_type(
    db: web::Data<DbPool>,
    payload: web::Json<CreateConnectorTypeDTO>,
) -> impl Responder {
    let repo = ConnectorTypeRepository::new(db.get_ref().clone());
    let command = CreateConnectorTypeCommand::new(repo);

    match command.execute(payload.name.clone(), payload.description.clone()).await {
        Ok(_) => HttpResponse::Created().finish(),
        Err(e) => e.error_response(),
    }
}

pub fn configure(cfg: &mut web::ServiceConfig) {
    cfg.service(get_all_connector_types);
    cfg.service(create_connector_type);
}
