use actix_web::{App, HttpServer, web, middleware::Logger};
use dotenvy::dotenv;

use crate::{
    api::routes::init_routes,
    infrastructure::{
        database::Pool,          // <- renamed from DbPoolWrapper
        cache::AppCaches,
        repositories::{
            station_repo::StationRepository,
            connector_status_repo::ConnectorStatusRepository,
            connector_type_repo::ConnectorTypeRepository,
        },
        logger,                   // <- use logger module directly
    },
    shared::config::Config,       // <- renamed from AppConfig
};
mod api;
mod application;
mod domain;
mod infrastructure;
mod shared;

/// Starts the Actix Web server with all routes and repositories
pub async fn start_server() -> std::io::Result<()> {
    dotenv().ok();
    logger::init(); // Initialize tracing/logging

    let config = Config::from_env();

    // Database pool
    let db_pool = Pool::new(&config.database_url)
        .await
        .expect("Failed to create DB pool");

    // Shared caches
    let caches = AppCaches::new();

    // Initialize repositories with shared cache
    let station_repo = StationRepository::new(db_pool.clone(), Some(caches.station_cache.clone()));
    let connector_status_repo = ConnectorStatusRepository::new(
        db_pool.clone(),
        Some(caches.connector_status_cache.clone()),
    );
    let connector_type_repo = ConnectorTypeRepository::new(
        db_pool.clone(),
        Some(caches.connector_type_cache.clone()),
    );

    log::info!("🚀 Starting server at {}:{}", config.server_host, config.server_port);

    HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(db_pool.clone()))
            .app_data(web::Data::new(station_repo.clone()))
            .app_data(web::Data::new(connector_status_repo.clone()))
            .app_data(web::Data::new(connector_type_repo.clone()))
            .wrap(Logger::default())
            .configure(init_routes)
    })
    .bind((config.server_host.clone(), config.server_port))?
    .run()
    .await
}
