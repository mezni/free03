use actix_web::{post, web, HttpResponse, Responder, ResponseError};
use serde::Deserialize;
use crate::services::auth_service::AuthService;
use crate::errors::AppError;

#[derive(Deserialize)]
pub struct AuthRequest {
    pub username: String,
    pub password: String,
}

#[post("/login")]
async fn login(
    auth_service: web::Data<AuthService>,
    req: web::Json<AuthRequest>,
) -> impl Responder {
    match auth_service.authenticate(&req.username, &req.password).await {
        Ok(user) => HttpResponse::Ok().json(user),
        Err(err) => err.error_response(), // Works because ResponseError is in scope
    }
}

// Initialize routes
pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(login);
}
