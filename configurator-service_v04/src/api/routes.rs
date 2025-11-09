use actix_web::web;

use crate::api::handlers::{
    network_handlers, 
    station_handlers, 
    connector_handlers, 
    session_handlers, 
    pricing_handlers
};

pub fn config(cfg: &mut web::ServiceConfig) {
    cfg
        // Health check
        .route("/health", web::get().to(health_check))
        
        // Networks routes
        .service(
            web::scope("/api/v1/networks")
                // Create network
                .route("", web::post().to(network_handlers::create_network))
                // List networks
                .route("", web::get().to(network_handlers::list_networks))
                // Get network by ID
                .route("/{id}", web::get().to(network_handlers::get_network))
                // Update network
                .route("/{id}", web::put().to(network_handlers::update_network))
                // Delete network
                .route("/{id}", web::delete().to(network_handlers::delete_network))
                // Create company for network
                .route("/{id}/company", web::post().to(network_handlers::create_company))
                // Get company for network
                .route("/{id}/company", web::get().to(network_handlers::get_company))
                // Update company
                .route("/{id}/company", web::put().to(network_handlers::update_company))
        )
        
        // Stations routes
        .service(
            web::scope("/api/v1/stations")
                // Create station
                .route("", web::post().to(station_handlers::create_station))
                // List stations
                .route("", web::get().to(station_handlers::list_stations))
                // Search stations near location
                .route("/search", web::get().to(station_handlers::search_stations))
                // Get station by ID
                .route("/{id}", web::get().to(station_handlers::get_station))
                // Update station
                .route("/{id}", web::put().to(station_handlers::update_station))
                // Delete station
                .route("/{id}", web::delete().to(station_handlers::delete_station))
                // Update station status
                .route("/{id}/status", web::put().to(station_handlers::update_station_status))
                // Get station with connectors
                .route("/{id}/connectors", web::get().to(station_handlers::get_station_with_connectors))
                // Update station availability
                .route("/{id}/availability", web::put().to(station_handlers::update_station_availability))
                // Check station availability
                .route("/{id}/availability/check", web::get().to(station_handlers::check_station_availability))
        )
        
        // Connectors routes
        .service(
            web::scope("/api/v1/connectors")
                // Create connector
                .route("", web::post().to(connector_handlers::create_connector))
                // Bulk create connectors
                .route("/bulk", web::post().to(connector_handlers::bulk_create_connectors))
                // Get connector by ID
                .route("/{id}", web::get().to(connector_handlers::get_connector))
                // Update connector status
                .route("/{id}/status", web::put().to(connector_handlers::update_connector_status))
                // Record connector maintenance
                .route("/{id}/maintenance", web::put().to(connector_handlers::record_maintenance))
                // Delete connector
                .route("/{id}", web::delete().to(connector_handlers::delete_connector))
                // List connectors by station
                .route("/station/{station_id}", web::get().to(connector_handlers::list_connectors_by_station))
                // List available connectors by station
                .route("/station/{station_id}/available", web::get().to(connector_handlers::list_available_connectors))
                // List connector types
                .route("/types", web::get().to(connector_handlers::list_connector_types))
                // List connector types by current type
                .route("/types/current/{current_type}", web::get().to(connector_handlers::list_connector_types_by_current))
        )
        
        // Sessions routes
        .service(
            web::scope("/api/v1/sessions")
                // Start charging session
                .route("", web::post().to(session_handlers::start_session))
                // Get session by ID
                .route("/{id}", web::get().to(session_handlers::get_session))
                // Complete charging session
                .route("/{id}/complete", web::put().to(session_handlers::complete_session))
                // Cancel charging session
                .route("/{id}/cancel", web::put().to(session_handlers::cancel_session))
                // Update session payment status
                .route("/{id}/payment", web::put().to(session_handlers::update_payment_status))
                // List sessions by user
                .route("/user/{user_id}", web::get().to(session_handlers::list_sessions_by_user))
                // List active sessions
                .route("/active", web::get().to(session_handlers::list_active_sessions))
                // Get session statistics
                .route("/statistics", web::get().to(session_handlers::get_session_statistics))
                // Get user session history
                .route("/user/{user_id}/history", web::get().to(session_handlers::get_user_session_history))
        )
        
        // Pricing routes
        .service(
            web::scope("/api/v1/pricing")
                // Create pricing rule
                .route("", web::post().to(pricing_handlers::create_pricing_rule))
                // List pricing rules by network
                .route("/network/{network_id}", web::get().to(pricing_handlers::list_pricing_rules))
                // Get pricing rule by ID
                .route("/{id}", web::get().to(pricing_handlers::get_pricing_rule))
                // Update pricing rule
                .route("/{id}", web::put().to(pricing_handlers::update_pricing_rule))
                // Deactivate pricing rule
                .route("/{id}/deactivate", web::put().to(pricing_handlers::deactivate_pricing_rule))
                // Delete pricing rule
                .route("/{id}", web::delete().to(pricing_handlers::delete_pricing_rule))
                // Get active pricing for network
                .route("/network/{network_id}/active", web::get().to(pricing_handlers::get_active_pricing))
                // Calculate cost
                .route("/calculate", web::post().to(pricing_handlers::calculate_cost))
                // Get pricing history
                .route("/network/{network_id}/history", web::get().to(pricing_handlers::get_pricing_history))
        );
}

async fn health_check() -> actix_web::HttpResponse {
    actix_web::HttpResponse::Ok().json(serde_json::json!({
        "status": "healthy",
        "timestamp": chrono::Utc::now().to_rfc3339()
    }))
}