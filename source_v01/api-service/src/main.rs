use actix_web::{web, App, HttpServer, HttpResponse};
use actix_files::Files;
use actix_cors::Cors;  // ADD THIS
use sqlx::{postgres::PgPoolOptions, Pool, Postgres};

mod handlers;
mod models;

use handlers::*;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenvy::dotenv().ok();
    
    let database_url = std::env::var("DATABASE_URL")
        .expect("DATABASE_URL must be set in .env file");
    
    println!("Attempting to connect to database...");
    
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .connect(&database_url)
        .await
        .expect("Failed to connect to database");

    println!("✅ Successfully connected to database!");
    println!("Starting server at http://127.0.0.1:5000");

    HttpServer::new(move || {
        // ADD CORS configuration
        let cors = Cors::default()
            .allow_any_origin()
            .allow_any_method()
            .allow_any_header()
            .max_age(3600);

        App::new()
            .wrap(cors)  // ADD THIS
            .app_data(web::Data::new(pool.clone()))
            // Test endpoint
            .route("/api/test", web::get().to(|| async {
                HttpResponse::Ok().json(serde_json::json!({
                    "success": true,
                    "message": "API is working"
                }))
            }))
            // Serve API endpoints
            .service(
                web::scope("/api/v1")
                    .route("/health", web::get().to(health_check))
                    .route("/stations/nearby", web::get().to(find_nearby_stations))
                    .route("/stations/{id}", web::get().to(get_station_by_id))
                    .route("/stations", web::get().to(get_all_stations))
                    .route("/stations/search", web::get().to(search_stations))
                    .route("/statistics", web::get().to(get_statistics))
                    .route("/connectors/types", web::get().to(get_connector_types))
                    .route("/export/geojson", web::get().to(export_geojson))
            )
            // Serve static files from frontend directory
            .service(Files::new("/", "./frontend").index_file("index.html"))
    })
    .bind("127.0.0.1:5000")?
    .run()
    .await
}

// Health check endpoint - return JSON
async fn health_check() -> HttpResponse {
    HttpResponse::Ok().json(serde_json::json!({
        "success": true,
        "message": "API is healthy"
    }))
}