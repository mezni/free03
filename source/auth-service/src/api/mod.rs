pub mod controllers;
pub mod middleware;
pub mod routes;
pub mod openapi;

// Re-exports
pub use controllers::{
    LoginRequest, RegisterRequest, TokenValidationRequest, RefreshTokenRequest,
    LogoutRequest, AssignRolesRequest, UpdateUserRequest,
    UserResponse, LoginResponse, TokenValidationResponse,
    AssignRolesResponse, CheckPermissionResponse
};
pub use routes::configure_routes;
pub use openapi::ApiDoc;