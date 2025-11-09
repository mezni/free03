pub mod routes;
pub mod handlers;
pub mod middleware;
pub mod models;
pub mod docs;

use axum::{
    Router,
    routing::{get, post, put, delete},
};
use tower::ServiceBuilder;
use tower_http::trace::TraceLayer;

use crate::application::services::EvChargingApplicationService;

pub fn create_api_router(app_service: EvChargingApplicationService) -> Router {
    let middleware_stack = ServiceBuilder::new()
        .layer(TraceLayer::new_for_http())
        .layer(middleware::authentication::AuthLayer::new())
        .layer(middleware::logging::LoggingLayer::new())
        .layer(middleware::error_handling::ErrorHandlingLayer::new());

    Router::new()
        // Health check
        .route("/health", get(routes::health::health_check))
        
        // Network routes
        .nest("/api/v1/networks", routes::networks::network_routes())
        
        // Station routes
        .nest("/api/v1/stations", routes::stations::station_routes())
        
        // Connector routes
        .nest("/api/v1/connectors", routes::connectors::connector_routes())
        
        // Session routes
        .nest("/api/v1/sessions", routes::sessions::session_routes())
        
        // Pricing routes
        .nest("/api/v1/pricing", routes::pricing::pricing_routes())
        
        // API documentation
        .nest("/api/docs", routes::docs::docs_routes())
        
        .layer(middleware_stack)
        .with_state(app_service)
}