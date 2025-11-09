pub mod connector_type_handlers;
pub mod connector_type_routes;
pub mod health_routes;
pub mod openapi;

pub use connector_type_handlers::*;
pub use health_routes::*;
pub use connector_type_routes::configure_connector_type_routes;
pub use health_routes::configure_health_routes;

use utoipa_swagger_ui::SwaggerUi;
use actix_web::web;
use utoipa::OpenApi; // Add this import

pub fn configure_routes(cfg: &mut web::ServiceConfig) {
    // Configure health routes first
    configure_health_routes(cfg);
    
    // Configure connector type routes
    configure_connector_type_routes(cfg);
    
    // Configure Swagger UI
    let openapi = openapi::ApiDoc::openapi();
    
    cfg.service(
        SwaggerUi::new("/swagger-ui/{_:.*}")
            .url("/api-docs/openapi.json", openapi),
    );
}