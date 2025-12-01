use crate::application::dtos::user::{CreateUserRequest, ErrorResponse, User, UserResponse};
use actix_web::{HttpResponse, Responder, get, post, web};

#[utoipa::path(
    get,
    path = "/api/users",
    tag = "Users",
    responses(
        (status = 200, description = "List of users", body = [User]),
        (status = 500, description = "Internal server error", body = ErrorResponse),
    )
)]
#[get("/api/users")]
pub async fn get_users_handler() -> impl Responder {
    let users: Vec<User> = Vec::new();
    HttpResponse::Ok().json(users)
}

#[utoipa::path(
    get,
    path = "/api/users/{id}",
    tag = "Users",
    params(
        ("id" = i32, Path, description = "User database ID")
    ),
    responses(
        (status = 200, description = "User found", body = UserResponse),
        (status = 404, description = "User not found", body = ErrorResponse),
    )
)]
#[get("/api/users/{id}")]
pub async fn get_user_handler(path: web::Path<i32>) -> impl Responder {
    let user_id = path.into_inner();

    HttpResponse::NotFound().json(ErrorResponse {
        status: "error",
        message: format!("User with ID {} not found", user_id),
    })
}

#[utoipa::path(
    post,
    path = "/api/users",
    tag = "Users",
    request_body = CreateUserRequest,
    responses(
        (status = 201, description = "User created successfully", body = UserResponse),
        (status = 400, description = "Invalid input", body = ErrorResponse),
    )
)]
#[post("/api/users")]
pub async fn create_user_handler(body: web::Json<CreateUserRequest>) -> impl Responder {
    let user = User {
        username: body.username.clone(),
        email: body.email.clone(),
    };

    HttpResponse::Created().json(UserResponse {
        status: "success",
        data: user,
    })
}
