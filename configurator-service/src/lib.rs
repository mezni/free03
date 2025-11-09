use actix_web::{App, HttpServer, web};
use infrastructure::config::Config;
use infrastructure::database::Database;
use infrastructure::logger::init_logger;
use std::sync::Arc;

// Application handlers
use application::commands::companies::{CompanyCommandHandler, CompanyCommandHandlerImpl};
use application::commands::networks::{NetworkCommandHandler, NetworkCommandHandlerImpl};
use application::commands::stations::{StationCommandHandler, StationCommandHandlerImpl};
use application::queries::companies::{CompanyQueryHandler, CompanyQueryHandlerImpl};
use application::queries::networks::{NetworkQueryHandler, NetworkQueryHandlerImpl};
use application::queries::stations::{StationQueryHandler, StationQueryHandlerImpl};

pub mod api;
pub mod application;
pub mod domain;
pub mod infrastructure;
pub mod shared;

// Re-exports for easier access
pub use shared::constants;
pub use shared::errors::AppError;

// Application state that will be shared across handlers
#[derive(Clone)]
pub struct AppState {
    pub db: infrastructure::database::Database,
    pub config: infrastructure::config::Config,
    pub network_command_handler: Arc<dyn NetworkCommandHandler>,
    pub company_command_handler: Arc<dyn CompanyCommandHandler>,
    pub station_command_handler: Arc<dyn StationCommandHandler>,
    pub network_query_handler: Arc<dyn NetworkQueryHandler>,
    pub company_query_handler: Arc<dyn CompanyQueryHandler>,
    pub station_query_handler: Arc<dyn StationQueryHandler>,
}

// Result type alias for the application
pub type Result<T> = std::result::Result<T, AppError>;

/// Create and configure the Actix Web application
pub async fn create_app() -> std::io::Result<actix_web::dev::Server> {
    // Initialize logger
    init_logger();

    // Load configuration
    let config = Config::from_env().expect("Failed to load configuration");

    // Initialize database connection pool
    let database = Database::new(&config.database_url)
        .await
        .expect("Failed to create database pool");

    // Create repositories
    let network_repository = Box::new(
        infrastructure::repositories::networks::NetworkRepositoryImpl::new(
            database.get_pool().clone(),
        ),
    );
    let company_repository = Box::new(
        infrastructure::repositories::companies::CompanyRepositoryImpl::new(
            database.get_pool().clone(),
        ),
    );
    let station_repository = Box::new(
        infrastructure::repositories::stations::StationRepositoryImpl::new(
            database.get_pool().clone(),
        ),
    );

    // Create command handlers - use Arc instead of Box
    let network_command_handler =
        Arc::new(NetworkCommandHandlerImpl::new(network_repository.clone()));
    let company_command_handler = Arc::new(CompanyCommandHandlerImpl::new(
        company_repository.clone(),
        network_repository.clone(),
    ));
    let station_command_handler = Arc::new(StationCommandHandlerImpl::new(
        station_repository.clone(),
        network_repository.clone(),
    ));

    // Create query handlers - use Arc instead of Box
    let network_query_handler = Arc::new(NetworkQueryHandlerImpl::new(network_repository));
    let company_query_handler = Arc::new(CompanyQueryHandlerImpl::new(company_repository));
    let station_query_handler = Arc::new(StationQueryHandlerImpl::new(station_repository));

    // Create application state
    let app_state = AppState {
        db: database,
        config: config.clone(),
        network_command_handler,
        company_command_handler,
        station_command_handler, // Add this
        network_query_handler,
        company_query_handler,
        station_query_handler, // Add this
    };

    log::info!("Starting server on {}:{}", config.host, config.port);

    // Build and return server
    let server = HttpServer::new(move || {
        App::new()
            .app_data(web::Data::new(app_state.clone()))
            .configure(api::routes::configure_routes)
    })
    .bind((config.host.as_str(), config.port))?
    .run();

    Ok(server)
}
