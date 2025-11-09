use actix_web::web;
use crate::api::connector_type_handlers::{
    list_connector_types, get_connector_type, create_connector_type, 
    update_connector_type, delete_connector_type
};

pub fn configure_connector_type_routes(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("/api/v1/connector-types")
            .route("", web::get().to(list_connector_types))
            .route("", web::post().to(create_connector_type))
            .route("/{id}", web::get().to(get_connector_type))
            .route("/{id}", web::put().to(update_connector_type))
            .route("/{id}", web::delete().to(delete_connector_type))
    );
}