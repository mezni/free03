use actix_web::{App, HttpServer};
use auth_service::config::AppConfig;
use auth_service::infra::logger;
use auth_service::repositories::{keycloak_repo::KeycloakRepo, cache_repo::CacheRepo};
use auth_service::services::auth_service::AuthService;
use auth_service::handlers::auth_handler;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    logger::init();

    // Load configuration
    let config = AppConfig::from_env();
    tracing::info!("Starting server at {}:{}", config.server_host, config.server_port);

    // Initialize repositories
    let keycloak_repo = KeycloakRepo::new(
        config.keycloak_url.clone(),
        config.keycloak_realm.clone(),
        config.keycloak_client_id.clone(),
        config.keycloak_client_secret.clone(),
    );
    let cache_repo = CacheRepo::new(config.cache_ttl_seconds);

    // Initialize AuthService
    let auth_service = AuthService::new(keycloak_repo, cache_repo);

    // Start Actix server
    HttpServer::new(move || {
        App::new()
            .app_data(actix_web::web::Data::new(auth_service.clone()))
            .configure(auth_handler::init)
    })
    .bind((config.server_host.as_str(), config.server_port))?
    .run()
    .await
}
