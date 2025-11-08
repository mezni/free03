use actix_web::web;
use actix_web::HttpResponse;
use utoipa::ToSchema;

#[derive(serde::Serialize, ToSchema)]
pub struct HealthResponse {
    pub status: String,
    pub service: String,
    pub timestamp: String,
}

#[derive(serde::Serialize, ToSchema)]
pub struct ServiceInfo {
    pub service: String,
    pub version: String,
    pub endpoints: Endpoints,
}

#[derive(serde::Serialize, ToSchema)]
pub struct Endpoints {
    pub connector_types: String,
    pub health: String,
    pub live: String,
    pub ready: String,
    pub swagger: String,
}

/// Get service information
#[utoipa::path(
    get,
    path = "/",
    tag = "health",
    responses(
        (status = 200, description = "Service information", body = ServiceInfo)
    )
)]
pub async fn index() -> HttpResponse {
    HttpResponse::Ok().json(ServiceInfo {
        service: "configurator-service".to_string(),
        version: env!("CARGO_PKG_VERSION").to_string(),
        endpoints: Endpoints {
            connector_types: "/api/v1/connector-types".to_string(),
            health: "/health".to_string(),
            live: "/health/live".to_string(),
            ready: "/health/ready".to_string(),
            swagger: "/swagger-ui/".to_string(),
        },
    })
}

/// Health check endpoint
#[utoipa::path(
    get,
    path = "/health",
    tag = "health",
    responses(
        (status = 200, description = "Service is healthy", body = HealthResponse)
    )
)]
pub async fn health_check() -> HttpResponse {
    HttpResponse::Ok().json(HealthResponse {
        status: "healthy".to_string(),
        service: "configurator-service".to_string(),
        timestamp: chrono::Utc::now().to_rfc3339(),
    })
}

/// Liveness probe
#[utoipa::path(
    get,
    path = "/health/live",
    tag = "health",
    responses(
        (status = 200, description = "Service is alive", body = HealthResponse)
    )
)]
pub async fn health_live() -> HttpResponse {
    HttpResponse::Ok().json(HealthResponse {
        status: "alive".to_string(),
        service: "configurator-service".to_string(),
        timestamp: chrono::Utc::now().to_rfc3339(),
    })
}

/// Readiness probe
#[utoipa::path(
    get,
    path = "/health/ready",
    tag = "health",
    responses(
        (status = 200, description = "Service is ready", body = HealthResponse)
    )
)]
pub async fn health_ready() -> HttpResponse {
    HttpResponse::Ok().json(HealthResponse {
        status: "ready".to_string(),
        service: "configurator-service".to_string(),
        timestamp: chrono::Utc::now().to_rfc3339(),
    })
}

pub fn configure_health_routes(cfg: &mut web::ServiceConfig) {
    cfg.service(
        web::scope("")
            .route("/", web::get().to(index))
            .route("/health", web::get().to(health_check))
            .route("/health/live", web::get().to(health_live))
            .route("/health/ready", web::get().to(health_ready))
    );
}