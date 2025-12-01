use serde::{Deserialize, Serialize};
use utoipa::ToSchema;

#[derive(Serialize, Deserialize, ToSchema)]
pub struct User {
    pub username: String,
    pub email: String,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct CreateUserRequest {
    pub username: String,
    pub email: String,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct UserResponse {
    pub status: &'static str,
    pub data: User,
}

#[derive(Serialize, Deserialize, ToSchema)]
pub struct ErrorResponse {
    pub status: &'static str,
    pub message: String,
}
