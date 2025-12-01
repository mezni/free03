use actix_web::{HttpResponse, Responder, get};
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Serialize, Deserialize, ToSchema)]
pub struct Response {
    pub status: &'static str,
    pub message: String,
}

#[utoipa::path(
    get,
    path = "/api/v1/healthchecker",
    tag = "Health Checker",
    responses(
        (status = 200, description = "API is healthy", body = Response),
    )
)]
#[get("/api/v1/healthchecker")]
pub async fn health_checker_handler() -> impl Responder {
    HttpResponse::Ok().json(Response {
        status: "success",
        message: "Complete Restful API in Rust".to_string(),
    })
}
