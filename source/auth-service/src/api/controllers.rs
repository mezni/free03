use actix_web::{web, HttpResponse};
use utoipa::ToSchema;
use validator::Validate;
use serde::{Deserialize, Serialize};

use crate::application::{
    AuthApplicationService,
    commands::{
        LoginCommand, RegisterCommand, AssignRolesCommand, ValidateTokenCommand,
        RefreshTokenCommand, LogoutCommand, UpdateUserCommand
    },
    queries::{
        GetUserQuery, GetUserRolesQuery, CheckPermissionQuery, GetUserPermissionsQuery
    },
    dtos::{
        UserDto, LoginResponse as AppLoginResponse, 
        TokenValidationResponse as AppTokenValidationResponse,
        UserResponse as AppUserResponse,
        AssignRolesResponse as AppAssignRolesResponse,
        CheckPermissionResponse as AppCheckPermissionResponse,
    },
};
use crate::shared::result::AppResult;
use crate::shared::types::{ApiResponse, HealthCheckResponse};
use crate::shared::result::{validation_error, not_found_error, unauthorized_error};

// Request DTOs
#[derive(Debug, Validate, Deserialize, ToSchema)]
pub struct LoginRequest {
    #[validate(length(min = 1, message = "Username is required"))]
    pub username: String,
    
    #[validate(length(min = 1, message = "Password is required"))]
    pub password: String,
}

#[derive(Debug, Validate, Deserialize, ToSchema)]
pub struct RegisterRequest {
    #[validate(email(message = "Invalid email format"))]
    pub email: String,
    
    #[validate(length(min = 1, max = 50, message = "Username must be between 1 and 50 characters"))]
    pub username: String,
    
    #[validate(length(min = 1, max = 100, message = "First name must be between 1 and 100 characters"))]
    pub first_name: String,
    
    #[validate(length(min = 1, max = 100, message = "Last name must be between 1 and 100 characters"))]
    pub last_name: String,
    
    #[validate(length(min = 8, message = "Password must be at least 8 characters long"))]
    pub password: String,
}

#[derive(Debug, Validate, Deserialize, ToSchema)]
pub struct TokenValidationRequest {
    #[validate(length(min = 1, message = "Token is required"))]
    pub token: String,
}

#[derive(Debug, Validate, Deserialize, ToSchema)]
pub struct RefreshTokenRequest {
    #[validate(length(min = 1, message = "Refresh token is required"))]
    pub refresh_token: String,
}

#[derive(Debug, Validate, Deserialize, ToSchema)]
pub struct LogoutRequest {
    #[validate(length(min = 1, message = "Refresh token is required"))]
    pub refresh_token: String,
}

#[derive(Debug, Validate, Deserialize, ToSchema)]
pub struct AssignRolesRequest {
    #[validate(length(min = 1, message = "At least one role is required"))]
    pub roles: Vec<String>,
}

#[derive(Debug, Validate, Deserialize, ToSchema)]
pub struct UpdateUserRequest {
    #[validate(length(min = 1, max = 100, message = "First name must be between 1 and 100 characters"))]
    pub first_name: Option<String>,
    
    #[validate(length(min = 1, max = 100, message = "Last name must be between 1 and 100 characters"))]
    pub last_name: Option<String>,
    
    pub enabled: Option<bool>,
}

// Response DTOs
#[derive(Debug, Serialize, ToSchema)]
pub struct LoginResponse {
    pub access_token: String,
    pub refresh_token: String,
    pub expires_in: i64,
    pub token_type: String,
    pub user: UserResponse,
}

#[derive(Debug, Serialize, ToSchema)]
pub struct TokenValidationResponse {
    pub valid: bool,
    pub user_id: Option<String>,
    pub username: Option<String>,
    pub email: Option<String>,
    pub roles: Vec<String>,
    pub permissions: Vec<String>,
    pub expires_at: Option<i64>,
}

#[derive(Debug, Serialize, ToSchema)]
pub struct UserResponse {
    pub id: String,
    pub email: String,
    pub username: String,
    pub first_name: String,
    pub last_name: String,
    pub full_name: String,
    pub enabled: bool,
    pub email_verified: bool,
    pub created_at: Option<i64>,
    pub updated_at: Option<i64>,
}

#[derive(Debug, Serialize, ToSchema)]
pub struct RoleResponse {
    pub id: String,
    pub name: String,
    pub description: Option<String>,
}

#[derive(Debug, Serialize, ToSchema)]
pub struct PermissionResponse {
    pub id: String,
    pub name: String,
    pub description: Option<String>,
    pub resource_type: Option<String>,
    pub scopes: Vec<String>,
}

#[derive(Debug, Serialize, ToSchema)]
pub struct AssignRolesResponse {
    pub user_id: String,
    pub assigned_roles: Vec<String>,
    pub message: String,
}

#[derive(Debug, Serialize, ToSchema)]
pub struct CheckPermissionResponse {
    pub has_permission: bool,
    pub user_id: String,
    pub permission: String,
}

// Controller functions

#[utoipa::path(
    post,
    path = "/api/v1/auth/login",
    request_body = LoginRequest,
    responses(
        (status = 200, description = "Login successful", body = ApiResponse<LoginResponse>),
        (status = 401, description = "Invalid credentials", body = ApiResponse<String>),
        (status = 400, description = "Invalid input", body = ApiResponse<String>)
    ),
    tag = "auth"
)]
pub async fn login(
    auth_service: web::Data<AuthApplicationService<crate::infrastructure::KeycloakClient>>,
    request: web::Json<LoginRequest>,
) -> AppResult<HttpResponse> {
    // Validate request
    request.validate()
        .map_err(|e| validation_error(&e.to_string()))?;

    // Create command
    let command = LoginCommand {
        username: request.username.clone(),
        password: request.password.clone(),
    };

    // Execute command
    let result = auth_service.login(command).await?;

    // Map to API response
    let api_response = ApiResponse::new(LoginResponse {
        access_token: result.access_token,
        refresh_token: result.refresh_token,
        expires_in: result.expires_in,
        token_type: result.token_type,
        user: UserResponse::from_dto(result.user),
    });

    Ok(HttpResponse::Ok().json(api_response))
}

#[utoipa::path(
    post,
    path = "/api/v1/auth/register",
    request_body = RegisterRequest,
    responses(
        (status = 201, description = "User registered successfully", body = ApiResponse<UserResponse>),
        (status = 400, description = "Invalid input", body = ApiResponse<String>),
        (status = 409, description = "User already exists", body = ApiResponse<String>)
    ),
    tag = "auth"
)]
pub async fn register(
    auth_service: web::Data<AuthApplicationService<crate::infrastructure::KeycloakClient>>,
    request: web::Json<RegisterRequest>,
) -> AppResult<HttpResponse> {
    // Validate request
    request.validate()
        .map_err(|e| validation_error(&e.to_string()))?;

    // Create command
    let command = RegisterCommand {
        email: request.email.clone(),
        username: request.username.clone(),
        first_name: request.first_name.clone(),
        last_name: request.last_name.clone(),
        password: request.password.clone(),
    };

    // Execute command
    let result = auth_service.register(command).await?;

    // Map to API response
    let api_response = ApiResponse::new(UserResponse::from_dto(result));

    Ok(HttpResponse::Created().json(api_response))
}

#[utoipa::path(
    post,
    path = "/api/v1/auth/validate",
    request_body = TokenValidationRequest,
    responses(
        (status = 200, description = "Token validation result", body = ApiResponse<TokenValidationResponse>),
        (status = 400, description = "Invalid input", body = ApiResponse<String>)
    ),
    tag = "auth"
)]
pub async fn validate_token(
    auth_service: web::Data<AuthApplicationService<crate::infrastructure::KeycloakClient>>,
    request: web::Json<TokenValidationRequest>,
) -> AppResult<HttpResponse> {
    // Validate request
    request.validate()
        .map_err(|e| validation_error(&e.to_string()))?;

    // Create command
    let command = ValidateTokenCommand {
        token: request.token.clone(),
    };

    // Execute command
    let result = auth_service.validate_token(command).await?;

    // Map to API response
    let api_response = ApiResponse::new(TokenValidationResponse::from_app_response(result));

    Ok(HttpResponse::Ok().json(api_response))
}

#[utoipa::path(
    post,
    path = "/api/v1/auth/refresh",
    request_body = RefreshTokenRequest,
    responses(
        (status = 200, description = "Token refreshed successfully", body = ApiResponse<LoginResponse>),
        (status = 400, description = "Invalid input", body = ApiResponse<String>),
        (status = 401, description = "Invalid refresh token", body = ApiResponse<String>)
    ),
    tag = "auth"
)]
pub async fn refresh_token(
    auth_service: web::Data<AuthApplicationService<crate::infrastructure::KeycloakClient>>,
    request: web::Json<RefreshTokenRequest>,
) -> AppResult<HttpResponse> {
    // Validate request
    request.validate()
        .map_err(|e| validation_error(&e.to_string()))?;

    // Create command
    let command = RefreshTokenCommand {
        refresh_token: request.refresh_token.clone(),
    };

    // Execute command
    let result = auth_service.refresh_token(command).await?;

    // Map to API response
    let api_response = ApiResponse::new(LoginResponse {
        access_token: result.access_token,
        refresh_token: result.refresh_token,
        expires_in: result.expires_in,
        token_type: result.token_type,
        user: UserResponse::default(), // We don't have user info here
    });

    Ok(HttpResponse::Ok().json(api_response))
}

#[utoipa::path(
    post,
    path = "/api/v1/auth/logout",
    request_body = LogoutRequest,
    responses(
        (status = 200, description = "Logout successful", body = ApiResponse<String>),
        (status = 400, description = "Invalid input", body = ApiResponse<String>)
    ),
    tag = "auth"
)]
pub async fn logout(
    auth_service: web::Data<AuthApplicationService<crate::infrastructure::KeycloakClient>>,
    request: web::Json<LogoutRequest>,
) -> AppResult<HttpResponse> {
    // Validate request
    request.validate()
        .map_err(|e| validation_error(&e.to_string()))?;

    // Create command
    let command = LogoutCommand {
        refresh_token: request.refresh_token.clone(),
    };

    // Execute command
    auth_service.logout(command).await?;

    let api_response = ApiResponse::with_message("".to_string(), "Logout successful");

    Ok(HttpResponse::Ok().json(api_response))
}

#[utoipa::path(
    get,
    path = "/api/v1/users/{user_id}",
    params(
        ("user_id" = String, Path, description = "User ID")
    ),
    responses(
        (status = 200, description = "User details", body = ApiResponse<UserResponse>),
        (status = 404, description = "User not found", body = ApiResponse<String>)
    ),
    tag = "users"
)]
pub async fn get_user(
    auth_service: web::Data<AuthApplicationService<crate::infrastructure::KeycloakClient>>,
    path: web::Path<String>,
) -> AppResult<HttpResponse> {
    let user_id = path.into_inner();

    // Create query
    let query = GetUserQuery { user_id: user_id.clone() };

    // Execute query
    let result = auth_service.get_user(query).await?;

    // Map to API response
    let api_response = ApiResponse::new(UserResponse::from_app_response(result));

    Ok(HttpResponse::Ok().json(api_response))
}

#[utoipa::path(
    put,
    path = "/api/v1/users/{user_id}",
    params(
        ("user_id" = String, Path, description = "User ID")
    ),
    request_body = UpdateUserRequest,
    responses(
        (status = 200, description = "User updated successfully", body = ApiResponse<UserResponse>),
        (status = 400, description = "Invalid input", body = ApiResponse<String>),
        (status = 404, description = "User not found", body = ApiResponse<String>)
    ),
    tag = "users"
)]
pub async fn update_user(
    auth_service: web::Data<AuthApplicationService<crate::infrastructure::KeycloakClient>>,
    path: web::Path<String>,
    request: web::Json<UpdateUserRequest>,
) -> AppResult<HttpResponse> {
    let user_id = path.into_inner();

    // Validate request
    request.validate()
        .map_err(|e| validation_error(&e.to_string()))?;

    // Create command
    let command = UpdateUserCommand {
        user_id,
        first_name: request.first_name.clone(),
        last_name: request.last_name.clone(),
        enabled: request.enabled,
    };

    // Execute command
    let result = auth_service.update_user(command).await?;

    // Map to API response
    let api_response = ApiResponse::new(UserResponse::from_dto(result));

    Ok(HttpResponse::Ok().json(api_response))
}

#[utoipa::path(
    post,
    path = "/api/v1/users/{user_id}/roles",
    params(
        ("user_id" = String, Path, description = "User ID")
    ),
    request_body = AssignRolesRequest,
    responses(
        (status = 200, description = "Roles assigned successfully", body = ApiResponse<AssignRolesResponse>),
        (status = 400, description = "Invalid input", body = ApiResponse<String>),
        (status = 404, description = "User not found", body = ApiResponse<String>)
    ),
    tag = "users"
)]
pub async fn assign_roles(
    auth_service: web::Data<AuthApplicationService<crate::infrastructure::KeycloakClient>>,
    path: web::Path<String>,
    request: web::Json<AssignRolesRequest>,
) -> AppResult<HttpResponse> {
    let user_id = path.into_inner();

    // Validate request
    request.validate()
        .map_err(|e| validation_error(&e.to_string()))?;

    // Create command
    let command = AssignRolesCommand {
        user_id: user_id.clone(),
        roles: request.roles.clone(),
    };

    // Execute command
    let result = auth_service.assign_roles(command).await?;

    // Map to API response
    let api_response = ApiResponse::new(AssignRolesResponse::from_app_response(result));

    Ok(HttpResponse::Ok().json(api_response))
}

#[utoipa::path(
    get,
    path = "/api/v1/users/{user_id}/roles",
    params(
        ("user_id" = String, Path, description = "User ID")
    ),
    responses(
        (status = 200, description = "User roles", body = ApiResponse<Vec<RoleResponse>>),
        (status = 404, description = "User not found", body = ApiResponse<String>)
    ),
    tag = "users"
)]
pub async fn get_user_roles(
    auth_service: web::Data<AuthApplicationService<crate::infrastructure::KeycloakClient>>,
    path: web::Path<String>,
) -> AppResult<HttpResponse> {
    let user_id = path.into_inner();

    // Create query
    let query = GetUserRolesQuery { user_id };

    // Execute query
    let result = auth_service.get_user_roles(query).await?;

    // Map to API response
    let api_response = ApiResponse::new(RoleResponse::from_dto_vec(result));

    Ok(HttpResponse::Ok().json(api_response))
}

#[utoipa::path(
    get,
    path = "/api/v1/users/{user_id}/permissions",
    params(
        ("user_id" = String, Path, description = "User ID")
    ),
    responses(
        (status = 200, description = "User permissions", body = ApiResponse<Vec<PermissionResponse>>),
        (status = 404, description = "User not found", body = ApiResponse<String>)
    ),
    tag = "users"
)]
pub async fn get_user_permissions(
    auth_service: web::Data<AuthApplicationService<crate::infrastructure::KeycloakClient>>,
    path: web::Path<String>,
) -> AppResult<HttpResponse> {
    let user_id = path.into_inner();

    // Create query
    let query = GetUserPermissionsQuery { user_id };

    // Execute query
    let result = auth_service.get_user_permissions(query).await?;

    // Map to API response
    let api_response = ApiResponse::new(PermissionResponse::from_dto_vec(result));

    Ok(HttpResponse::Ok().json(api_response))
}

#[utoipa::path(
    get,
    path = "/api/v1/users/{user_id}/permissions/{permission}",
    params(
        ("user_id" = String, Path, description = "User ID"),
        ("permission" = String, Path, description = "Permission to check")
    ),
    responses(
        (status = 200, description = "Permission check result", body = ApiResponse<CheckPermissionResponse>),
        (status = 404, description = "User not found", body = ApiResponse<String>)
    ),
    tag = "users"
)]
pub async fn check_permission(
    auth_service: web::Data<AuthApplicationService<crate::infrastructure::KeycloakClient>>,
    path: web::Path<(String, String)>,
) -> AppResult<HttpResponse> {
    let (user_id, permission) = path.into_inner();

    // Create query
    let query = CheckPermissionQuery { user_id: user_id.clone(), permission: permission.clone() };

    // Execute query
    let result = auth_service.check_permission(query).await?;

    // Map to API response
    let api_response = ApiResponse::new(CheckPermissionResponse::from_app_response(result));

    Ok(HttpResponse::Ok().json(api_response))
}

#[utoipa::path(
    get,
    path = "/api/v1/health",
    responses(
        (status = 200, description = "Service health status", body = HealthCheckResponse)
    ),
    tag = "system"
)]
pub async fn health_check() -> HttpResponse {
    let health = HealthCheckResponse::default();
    HttpResponse::Ok().json(health)
}

// Implementation of conversion traits

impl UserResponse {
    pub fn from_domain(user: crate::domain::user::User) -> Self {
        // Clone the values or use references to avoid partial move
        let full_name = user.get_full_name();
        
        Self {
            id: user.id,
            email: user.email,
            username: user.username,
            first_name: user.first_name,  // This moves first_name
            last_name: user.last_name,    // This moves last_name
            full_name,                    // full_name is already computed
            enabled: user.enabled,
            email_verified: user.email_verified,
            created_at: user.created_at,
            updated_at: user.updated_at,
        }
    }

    pub fn from_dto(dto: UserDto) -> Self {
        Self {
            id: dto.id,
            email: dto.email,
            username: dto.username,
            first_name: dto.first_name,
            last_name: dto.last_name,
            full_name: dto.full_name,
            enabled: dto.enabled,
            email_verified: dto.email_verified,
            created_at: dto.created_at,
            updated_at: dto.updated_at,
        }
    }

    pub fn from_app_response(response: AppUserResponse) -> Self {
        Self::from_dto(response.user)
    }

    pub fn default() -> Self {
        Self {
            id: "".to_string(),
            email: "".to_string(),
            username: "".to_string(),
            first_name: "".to_string(),
            last_name: "".to_string(),
            full_name: "".to_string(),
            enabled: false,
            email_verified: false,
            created_at: None,
            updated_at: None,
        }
    }
}

impl RoleResponse {
    pub fn from_dto(dto: crate::application::dtos::RoleDto) -> Self {
        Self {
            id: dto.id,
            name: dto.name,
            description: dto.description,
        }
    }

    pub fn from_dto_vec(dtos: Vec<crate::application::dtos::RoleDto>) -> Vec<Self> {
        dtos.into_iter().map(Self::from_dto).collect()
    }
}

impl PermissionResponse {
    pub fn from_dto(dto: crate::application::dtos::PermissionDto) -> Self {
        Self {
            id: dto.id,
            name: dto.name,
            description: dto.description,
            resource_type: dto.resource_type,
            scopes: dto.scopes,
        }
    }

    pub fn from_dto_vec(dtos: Vec<crate::application::dtos::PermissionDto>) -> Vec<Self> {
        dtos.into_iter().map(Self::from_dto).collect()
    }
}

impl TokenValidationResponse {
    pub fn from_app_response(response: AppTokenValidationResponse) -> Self {
        Self {
            valid: response.valid,
            user_id: response.user_id,
            username: response.username,
            email: response.email,
            roles: response.roles,
            permissions: response.permissions,
            expires_at: response.expires_at,
        }
    }
}

impl AssignRolesResponse {
    pub fn from_app_response(response: AppAssignRolesResponse) -> Self {
        Self {
            user_id: response.user_id,
            assigned_roles: response.assigned_roles,
            message: response.message,
        }
    }
}

impl CheckPermissionResponse {
    pub fn from_app_response(response: AppCheckPermissionResponse) -> Self {
        Self {
            has_permission: response.has_permission,
            user_id: response.user_id,
            permission: response.permission,
        }
    }
}