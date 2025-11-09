pub mod connector_status_routes;
pub mod connector_type_routes;
pub mod station_routes;

use actix_web::web;

/// Initializes all routes for the API
pub fn init_routes(cfg: &mut web::ServiceConfig) {
    connector_type_routes::init(cfg);
    connector_status_routes::init(cfg);
    station_routes::init(cfg);
}
