use actix_web::web;
use actix_web_httpauth::middleware::HttpAuthentication;

use crate::api::controllers;
use crate::api::middleware;

pub fn configure_routes(cfg: &mut web::ServiceConfig) {
    // Authentication middleware - using simple validator for now
    let auth_middleware = HttpAuthentication::bearer(middleware::validator);

    // System routes (no authentication)
    cfg.service(
        web::scope("/api/v1")
            .route("/health", web::get().to(controllers::health_check))
    );

    // Auth routes (no authentication required)
    cfg.service(
        web::scope("/api/v1/auth")
            .route("/login", web::post().to(controllers::login))
            .route("/register", web::post().to(controllers::register))
            .route("/validate", web::post().to(controllers::validate_token))
            .route("/refresh", web::post().to(controllers::refresh_token))
            .route("/logout", web::post().to(controllers::logout))
    );

    // User routes (authentication required)
    cfg.service(
        web::scope("/api/v1/users")
            .wrap(auth_middleware)
            .route("/{user_id}", web::get().to(controllers::get_user))
            .route("/{user_id}", web::put().to(controllers::update_user))
            .route("/{user_id}/roles", web::get().to(controllers::get_user_roles))
            .route("/{user_id}/permissions", web::get().to(controllers::get_user_permissions))
            .route("/{user_id}/permissions/{permission}", web::get().to(controllers::check_permission))
            .route("/{user_id}/roles", web::post().to(controllers::assign_roles))
    );
}