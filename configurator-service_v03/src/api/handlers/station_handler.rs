use actix_web::{get, post, web, HttpResponse, Responder};
use chrono::Utc;
use crate::{
    application::commands::station_commands::CreateStationCommand,
    application::queries::station_queries::GetStationsQuery,
    infrastructure::repositories::station_repo::StationRepository,
    infrastructure::database::DbPool,
    shared::errors::AppError,
};
use crate::api::dtos::station_dto::{StationDTO, CreateStationDTO};

#[get("/")]
pub async fn get_all_stations(db: web::Data<DbPool>) -> impl Responder {
    let repo = StationRepository::new(db.get_ref().clone());
    let query = GetStationsQuery::new(repo);

    match query.execute(100, 0).await { // default limit & offset
        Ok(stations) => HttpResponse::Ok().json(stations),
        Err(e) => e.error_response(),
    }
}

#[post("/")]
pub async fn create_station(
    db: web::Data<DbPool>,
    payload: web::Json<CreateStationDTO>,
) -> impl Responder {
    let repo = StationRepository::new(db.get_ref().clone());
    let command = CreateStationCommand::new(repo);

    match command.execute(
        payload.osm_id,
        payload.name.clone(),
        payload.address.clone(),
        payload.operator.clone(),
    ).await {
        Ok(_) => HttpResponse::Created().finish(),
        Err(e) => e.error_response(),
    }
}

pub fn configure(cfg: &mut web::ServiceConfig) {
    cfg.service(get_all_stations);
    cfg.service(create_station);
}
