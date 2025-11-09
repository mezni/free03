use actix_web::web;
use utoipa::OpenApi;
use utoipa_swagger_ui::SwaggerUi;

use crate::api::handlers::init_handlers;
use crate::api::openapi::ApiDoc;

/// Registers all application routes and Swagger/OpenAPI documentation.
pub fn configure_routes(cfg: &mut web::ServiceConfig) {
    // Register all application handlers (endpoints)
    init_handlers(cfg);

    // Register Swagger UI for API documentation
    cfg.service(
        SwaggerUi::new("/docs/{_:.*}")
            .url("/api-docs/openapi.json", ApiDoc::openapi()),
    );
}
