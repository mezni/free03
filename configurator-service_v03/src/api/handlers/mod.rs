pub mod connector_type_handler;
pub mod connector_status_handler;
pub mod station_handler;

use actix_web::web;

/// Registers all handler routes under a single scope.
/// This function will be called in `routes/mod.rs` when building the app.
pub fn init_handlers(cfg: &mut web::ServiceConfig) {
    connector_type_handler::configure(cfg);
    connector_status_handler::configure(cfg);
    station_handler::configure(cfg);
}
