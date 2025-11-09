use actix_web::web;
use crate::api::handlers::connector_type_handler;

pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("/api/v1/connector-types")
            .route("", web::get().to(connector_type_handler::get_all_connector_types))
            .route("", web::post().to(connector_type_handler::create_connector_type))
    );
}
