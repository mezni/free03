use actix_web::{HttpResponse, Responder, get, post, web};
use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Serialize, Deserialize, ToSchema)]
pub struct User {
    pub username: String,
    pub email: String,
}

#[utoipa::path(
    get,
    path = "/api/users",
    tag = "Users",
    responses(
        (status = 200, description = "List of users", body = [User]),
    )
)]
#[get("/api/users")]
pub async fn get_users_handler() -> impl Responder {
    let users: Vec<User> = Vec::new();
    HttpResponse::Ok().json(users)
}
