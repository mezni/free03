#!/bin/bash

set -e

PROJECT_NAME="configurator-service"

echo "Creating project structure for $PROJECT_NAME..."

mkdir $PROJECT_NAME
cd $PROJECT_NAME

# Create directory structure
mkdir -p src/{infrastructure,application,interfaces/http}

# Create Cargo.toml
cat > Cargo.toml << 'EOF'
[package]
name = "configurator-service"
version = "0.1.0"
edition = "2021"

[dependencies]
actix-web = "4.12.1"
anyhow = "1.0.100"
dotenvy = "0.15.7"
serde = "1.0.228"
serde_json = "1.0.145"
sqlx = "0.8.6"
thiserror = "2.0.17"
tracing = "0.1.43"
tracing-subscriber = { version = "0.3.22", features = ["env-filter", "time"] }
utoipa = { version = "5.4.0", features = ["actix_extras"] }
utoipa-swagger-ui = { version = "9.0.2", features = ["actix-web", "debug-embed"] }
chrono = { version = "0.4", features = ["serde"] }
EOF

# Create .env file
cat > .env << 'EOF'
HOST=127.0.0.1
PORT=8080
LOG_LEVEL=info
RUST_LOG=info
EOF

# Create src/main.rs
cat > src/main.rs << 'EOF'
use configurator_service::run;

#[actix_web::main]
async fn main() -> Result<(), anyhow::Error> {
    run().await
}
EOF

# Create src/lib.rs
cat > src/lib.rs << 'EOF'
pub mod error;
pub mod infrastructure;
pub mod application;
pub mod interfaces;
pub mod auth;
pub mod types;

use actix_web::{middleware, web, App, HttpServer};
use tracing::info;
use infrastructure::config::Config;
use utoipa_swagger_ui::SwaggerUi;

use crate::interfaces::http::ApiDoc;

fn config(conf: &mut web::ServiceConfig) {
    let scope = web::scope("/api")
        .service(interfaces::http::handlers::index)
        .service(interfaces::http::handlers::auth_index)
        .service(interfaces::http::handlers::create_thing)
        .service(interfaces::http::handlers::delete_thing);
    conf.service(scope);
}

pub async fn run() -> Result<(), anyhow::Error> {
    dotenvy::dotenv().ok();
    let config = Config::load()?;
    infrastructure::logger::init(&config);
    
    info!("Starting server on {}:{}", config.host, config.port);
    info!("App version: {}", env!("CARGO_PKG_VERSION"));

    HttpServer::new(|| {
        App::new()
            // Enable logger
            .wrap(middleware::Logger::default())
            .configure(config)
            // Add Swagger UI
            .service(
                SwaggerUi::new("/swagger-ui/{_:.*}")
                    .url("/api-docs/openapi.json", ApiDoc::openapi()),
            )
    })
    .bind((config.host.as_str(), config.port))?
    .run()
    .await
    .map_err(|e| anyhow::anyhow!("Server error: {}", e))
}

pub use error::AppError;
EOF

# Create src/error.rs
cat > src/error.rs << 'EOF'
use actix_web::{HttpResponse, ResponseError};
use serde::Serialize;
use thiserror::Error;
use tracing::error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("Configuration error: {0}")]
    Config(String),
    
    #[error("Validation error: {0}")]
    Validation(String),
    
    #[error("Not found: {0}")]
    NotFound(String),
    
    #[error("Internal server error")]
    Internal,
    
    #[error("Authentication error: {0}")]
    Auth(String),
}

#[derive(Serialize)]
pub struct ErrorResponse {
    pub error: String,
    pub code: String,
}

impl ResponseError for AppError {
    fn error_response(&self) -> HttpResponse {
        error!("Error occurred: {}", self);
        
        match self {
            AppError::Config(_) => HttpResponse::InternalServerError().json(ErrorResponse {
                error: "Configuration error".to_string(),
                code: "CONFIG_ERROR".to_string(),
            }),
            AppError::Validation(msg) => HttpResponse::BadRequest().json(ErrorResponse {
                error: msg.to_string(),
                code: "VALIDATION_ERROR".to_string(),
            }),
            AppError::NotFound(msg) => HttpResponse::NotFound().json(ErrorResponse {
                error: msg.to_string(),
                code: "NOT_FOUND".to_string(),
            }),
            AppError::Internal => HttpResponse::InternalServerError().json(ErrorResponse {
                error: "Internal server error".to_string(),
                code: "INTERNAL_ERROR".to_string(),
            }),
            AppError::Auth(msg) => HttpResponse::Unauthorized().json(ErrorResponse {
                error: msg.to_string(),
                code: "AUTH_ERROR".to_string(),
            }),
        }
    }
}

impl From<anyhow::Error> for AppError {
    fn from(err: anyhow::Error) -> Self {
        error!("Anyhow error converted to AppError: {}", err);
        AppError::Internal
    }
}

pub type Result<T> = std::result::Result<T, AppError>;
EOF

# Create src/auth.rs
cat > src/auth.rs << 'EOF'
use std::{future::Future, pin::Pin};

use actix_web::{http::header, FromRequest, HttpMessage};
use serde::{Deserialize, Serialize};

#[derive(Serialize, Deserialize, Debug, Default, Clone)]
pub struct AuthToken(String);

impl FromRequest for AuthToken {
    type Error = actix_web::Error;
    type Future = Pin<Box<dyn Future<Output = Result<Self, Self::Error>>>>;

    fn from_request(req: &actix_web::HttpRequest, _: &mut actix_web::dev::Payload) -> Self::Future {
        match get_auth_token_from_header(req) {
            Ok("super-secret-password") => {
                Box::pin(async move { Ok(AuthToken("super-secret-password".into())) })
            }
            _ => Box::pin(async move { Err(actix_web::error::ErrorUnauthorized("Invalid")) }),
        }
    }
}

fn get_auth_token_from_header(req: &impl HttpMessage) -> Result<&str, &str> {
    req.headers()
        .get(header::AUTHORIZATION)
        .and_then(|t| t.to_str().ok())
        .and_then(|t| t.strip_prefix("Bearer "))
        .ok_or("missing error")
}
EOF

# Create src/types.rs
cat > src/types.rs << 'EOF'
use serde::{Deserialize, Serialize};
use utoipa::{IntoParams, ToSchema};

#[derive(ToSchema, Serialize, Deserialize, Debug, PartialEq, Eq)]
#[aliases(
    GenericPostResponse = GenericResponse<PostResponse>,
    GenericStringResponse = GenericResponse<String>
)]
pub struct GenericResponse<U> {
    pub msg: String,
    pub data: U,
}

use utoipa::TupleUnit;

#[derive(ToSchema, Serialize, Deserialize, Debug, PartialEq, Eq)]
#[aliases(
    GenericPostRequest = GenericRequest<TupleUnit, PostRequest>,
    GenericDeleteRequest = GenericRequest<TupleUnit, DeleteRequest>,
)]
pub struct GenericRequest<U, V> {
    pub params: Option<U>,
    pub data: Option<V>,
}

#[derive(ToSchema, Serialize, Deserialize, Debug, PartialEq, Eq)]
pub struct PostRequest {
    pub name: String,
}

#[derive(ToSchema, Serialize, Deserialize, Debug, PartialEq, Eq)]
pub struct PostResponse {
    pub status: String,
}

#[derive(IntoParams, Serialize, Deserialize, Debug, PartialEq, Eq)]
pub struct DeleteRequest {
    /// Delete Permanently ?
    pub permanent: Option<bool>,

    /// when to delete ?
    pub when: Option<u64>,

    /// height of shamelessness
    pub height: u64,
}
EOF

# Create infrastructure files
cat > src/infrastructure/mod.rs << 'EOF'
pub mod config;
pub mod logger;
EOF

cat > src/infrastructure/config.rs << 'EOF'
use serde::Deserialize;
use tracing::info;

#[derive(Debug, Deserialize, Clone)]
pub struct Config {
    pub host: String,
    pub port: u16,
    pub log_level: String,
}

impl Config {
    pub fn load() -> Result<Self, anyhow::Error> {
        info!("Loading configuration...");
        
        let host = std::env::var("HOST")
            .unwrap_or_else(|_| "127.0.0.1".to_string());
            
        let port = std::env::var("PORT")
            .unwrap_or_else(|_| "8080".to_string())
            .parse()
            .map_err(|e| anyhow::anyhow!("Invalid PORT: {}", e))?;
            
        let log_level = std::env::var("LOG_LEVEL")
            .unwrap_or_else(|_| "info".to_string());

        Ok(Config {
            host,
            port,
            log_level,
        })
    }
}
EOF

cat > src/infrastructure/logger.rs << 'EOF'
use tracing_subscriber::{fmt, EnvFilter};
use super::config::Config;

pub fn init(config: &Config) {
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new(&config.log_level));

    tracing_subscriber::fmt()
        .with_env_filter(filter)
        .with_target(true)
        .with_timer(fmt::time::UtcTime::rfc_3339())
        .init();

    tracing::info!("Logger initialized with level: {}", config.log_level);
}
EOF

# Create application files
cat > src/application/mod.rs << 'EOF'
// Business logic modules will go here
EOF

# Create interfaces files
cat > src/interfaces/mod.rs << 'EOF'
pub mod http;
EOF

cat > src/interfaces/http/mod.rs << 'EOF'
pub mod handlers;
pub mod swagger_docs;

pub use swagger_docs::ApiDoc;
EOF

cat > src/interfaces/http/handlers.rs << 'EOF'
use actix_web::{delete, get, http::StatusCode, post, web, HttpRequest, HttpResponse};
use crate::{
    auth::AuthToken,
    types::{DeleteRequest, GenericRequest, GenericResponse, PostRequest, PostResponse},
};

/// Root Endpoint
///
/// Hello World Example
#[utoipa::path(
    context_path = "/api",
    responses(
        (status = 200, description = "Hello World!")
    )
)]
#[get("/")]
pub async fn index(req: HttpRequest) -> &'static str {
    println!("REQ: {req:?}");
    "Hello world!"
}

/// Auth Endpoint
///
/// Basic Auth Example (password is `super-secret-password`)
#[utoipa::path(
    context_path = "/api",
    responses(
        (status = 200, description = "Hello World!"),
        (status = 401, description = "Invalid")
    ),
    security(
        ("Token" = []),
    )
)]
#[get("/auth")]
pub async fn auth_index(_: AuthToken, req: HttpRequest) -> &'static str {
    println!("REQ: {req:?}");
    "Hello world!"
}

/// Post Endpoint
///
/// Basic Post Example
#[utoipa::path(
    context_path = "/api",
    responses(
        (status = 200, description = "Success", body = GenericPostResponse),
        (status = 409, description = "Invalid Request Format")
    ),
    request_body = GenericPostRequest,
)]
#[post("/create")]
pub async fn create_thing(
    req: HttpRequest,
    mut request: web::Json<GenericRequest<(), PostRequest>>,
) -> HttpResponse {
    println!("REQ: {req:?}");

    let name = format!(
        "success: {}",
        request
            .data
            .take()
            .map(|d| d.name)
            .unwrap_or("failed".into())
    );
    let resp = PostResponse { status: name };
    let resp: GenericResponse<PostResponse> = GenericResponse {
        msg: "success".into(),
        data: resp,
    };
    HttpResponse::Ok()
        .content_type("application/json")
        .status(StatusCode::OK)
        .json(resp)
}

/// Delete Endpoint
///
/// Basic Delete Example
#[utoipa::path(
    context_path = "/api",
    responses(
        (status = 200, description = "Success", body = GenericStringResponse),
        (status = 409, description = "Invalid Request Format")
    ),
    params(
        ("email" = String, Path, description = "User email"),
        DeleteRequest,
    ),
)]
#[delete("/delete/{email}")]
pub async fn delete_thing(
    req: HttpRequest,
    query: web::Query<DeleteRequest>,
    path: web::Path<String>,
) -> HttpResponse {
    println!("REQ: {req:?}");

    let query = query.into_inner();
    let resp: GenericResponse<String> = GenericResponse {
        msg: "Success".into(),
        data: format!(
            "email: {} permanent: {:#?}, when: {:#?}, height: {}",
            path,
            query.permanent.unwrap_or(false),
            query.when.unwrap_or(64),
            query.height
        ),
    };

    HttpResponse::Ok()
        .content_type("application/json")
        .status(StatusCode::OK)
        .json(resp)
}
EOF

cat > src/interfaces/http/swagger_docs.rs << 'EOF'
use utoipa::{
    openapi::{
        self,
        security::{Http, HttpAuthScheme, SecurityScheme},
    },
    Modify, OpenApi,
};

use crate::types;

#[derive(OpenApi)]
#[openapi(
    paths(
        crate::interfaces::http::handlers::index,
        crate::interfaces::http::handlers::auth_index,
        crate::interfaces::http::handlers::create_thing,
        crate::interfaces::http::handlers::delete_thing,
    ),
    components(
        schemas(
            utoipa::TupleUnit,
            types::GenericPostRequest,
            types::GenericPostResponse,
            types::GenericStringResponse,
            types::PostRequest,
            types::PostResponse,
        )
    ),
    tags((name = "BasicAPI", description = "A very Basic API")),
    modifiers(&SecurityAddon)
)]
pub struct ApiDoc;

struct SecurityAddon;

impl Modify for SecurityAddon {
    fn modify(&self, openapi: &mut openapi::OpenApi) {
        if let Some(components) = openapi.components.as_mut() {
            components.add_security_scheme(
                "Token",
                SecurityScheme::Http(Http::new(HttpAuthScheme::Bearer)),
            );
        }
    }
}
EOF

# Create README.md
cat > README.md << 'EOF'
# My Actix Web App

A Rust Actix Web application with Clean Architecture, Swagger documentation, and authentication.

## Features

- Actix Web 4.0
- Clean Architecture organization
- Swagger/OpenAPI documentation
- JWT-like authentication
- Structured error handling
- Configuration management
- Logging with tracing

## Endpoints

- `GET /api/` - Hello world
- `GET /api/auth` - Auth endpoint (Bearer token: "super-secret-password")
- `POST /api/create` - Create thing
- `DELETE /api/delete/{email}` - Delete thing
- `GET /swagger-ui/` - Swagger UI documentation

## Getting Started

1. Run the project:
```bash
cargo run
EOF