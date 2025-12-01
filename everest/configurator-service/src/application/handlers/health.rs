use crate::application::dtos::health::HealthResponse;
use actix_web::{HttpResponse, Responder, get};

#[utoipa::path(
    get,
    path = "/api/healthchecker",
    tag = "Health Checker",
    responses(
        (status = 200, description = "Health check successful", body = HealthResponse),       
    )
)]
#[get("/api/healthchecker")]
pub async fn health_checker_handler() -> impl Responder {
    HttpResponse::Ok().json(HealthResponse {
        status: "success",
        message: "Complete Restful API in Rust".to_string(),
    })
}
