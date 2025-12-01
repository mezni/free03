use actix_web::{App, HttpServer, middleware::Logger};
use anyhow::Context;
use std::env;
use utoipa::OpenApi;

pub mod application;
pub mod errors;
pub mod interfaces;

use crate::application::handlers::health::health_checker_handler;
use crate::interfaces::http::openapi::ApiDoc;

#[derive(Clone)]
pub struct AppState {
    pub app_name: String,
}

pub async fn run() -> anyhow::Result<()> {
    dotenvy::dotenv().context("Failed to load .env file")?;

    let port = env::var("PORT")
        .unwrap_or_else(|_| "3000".into())
        .parse::<u16>()
        .context("PORT must be a valid number")?;

    env_logger::init();

    println!("Server running on http://localhost:{port}");

    let openapi = ApiDoc::openapi();

    let state = AppState {
        app_name: "Rust REST API".to_string(),
    };

    HttpServer::new(move || {
        App::new()
            .app_data(actix_web::web::Data::new(state.clone()))
            .wrap(Logger::default())
            .service(health_checker_handler)
            .service(
                utoipa_swagger_ui::SwaggerUi::new("/swagger-ui/{_:.*}")
                    .url("/api-docs/openapi.json", openapi.clone()),
            )
    })
    .bind(("0.0.0.0", port))
    .context("Failed to bind server port")?
    .run()
    .await
    .context("Server failed to start")
}
