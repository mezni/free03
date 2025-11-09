use configurator_service::{Config, run_server};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Load configuration with proper fallback
    let config = Config::from_env().unwrap_or_default();
    
    println!("🚀 Starting Configurator Service...");
    println!("🌐 Server will be available at: http://{}", config.server_address());
    println!("📚 Swagger UI will be at: http://{}/docs/", config.server_address());
    println!("🔧 Health check: http://{}/health", config.server_address());
    println!("📊 Database: {}", config.database_url);
    println!("💾 Cache capacity: {}", config.cache_capacity);
    
    // Run the server
    run_server(config).await
}