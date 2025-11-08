pub mod shared;
pub mod domain;
pub mod infrastructure;
pub mod application;
pub mod api;
pub mod config;
pub mod logger;

use actix_web::{web, App, HttpServer};
use std::io::Result;
use std::sync::Arc;
use utoipa_swagger_ui::SwaggerUi; // Add this import
use utoipa::OpenApi; // Add this import

pub use config::Config;
pub use logger::init_logger;

pub async fn run_server(config: Config) -> Result<()> {
    init_logger();
    
    log::info!("🚀 Starting Configurator Service on {}", config.server_address());
    log::info!("📊 Database URL: {}", config.database_url);
    
    // Set up database connection
    let pool = match sqlx::postgres::PgPool::connect(&config.database_url).await {
        Ok(pool) => {
            log::info!("✅ Connected to database successfully");
            pool
        }
        Err(e) => {
            log::error!("❌ Failed to connect to database: {}", e);
            log::info!("Please check your DATABASE_URL and ensure PostgreSQL is running");
            std::process::exit(1);
        }
    };
    
    // Test database connection
    match sqlx::query("SELECT 1").execute(&pool).await {
        Ok(_) => log::info!("✅ Database connection test successful"),
        Err(e) => {
            log::error!("❌ Database connection test failed: {}", e);
            std::process::exit(1);
        }
    }
    
    // Initialize cache
    let cache = Arc::new(shared::cache::create_connector_type_cache(
        config.cache_capacity,
        config.cache_ttl_seconds,
    ));
    log::info!("✅ Cache initialized with capacity: {}", config.cache_capacity);
    
    // Initialize repository
    let connector_type_repo = infrastructure::ConnectorTypeRepositoryImpl::new(pool);
    
    // Initialize commands and queries
    let create_command = application::CreateConnectorTypeCommand::new(connector_type_repo.clone());
    let update_command = application::UpdateConnectorTypeCommand::new(connector_type_repo.clone());
    let delete_command = application::DeleteConnectorTypeCommand::new(connector_type_repo.clone());
    let list_query = application::ListConnectorTypesQuery::new(connector_type_repo.clone());
    let get_by_id_query = application::GetConnectorTypeByIdQuery::new(connector_type_repo, cache);
    
    log::info!("✅ Application initialized successfully");
    log::info!("🌐 Server starting on {}", config.server_address());
    log::info!("📚 Swagger UI available at: http://{}/swagger-ui/", config.server_address());
    
    HttpServer::new(move || {
        let openapi = crate::api::openapi::ApiDoc::openapi();
        
        App::new()
            .app_data(web::Data::new(get_by_id_query.clone()))
            .app_data(web::Data::new(list_query.clone()))
            .app_data(web::Data::new(create_command.clone()))
            .app_data(web::Data::new(update_command.clone()))
            .app_data(web::Data::new(delete_command.clone()))
            .configure(api::configure_routes)
            // Manual Swagger registration as backup
            .service(
                SwaggerUi::new("/swagger-ui/{_:.*}")
                    .url("/api-docs/openapi.json", openapi),
            )
    })
    .bind(config.server_address())?
    .run()
    .await
}