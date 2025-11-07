use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(
    paths(
        crate::api::controllers::health_check,
        crate::api::controllers::login,
        crate::api::controllers::register,
        crate::api::controllers::validate_token,
        crate::api::controllers::refresh_token,
        crate::api::controllers::logout,
        crate::api::controllers::get_user,
        crate::api::controllers::update_user,
        crate::api::controllers::assign_roles,
        crate::api::controllers::get_user_roles,
        crate::api::controllers::get_user_permissions,
        crate::api::controllers::check_permission,
    ),
    components(
        schemas(
            // Request schemas
            crate::api::controllers::LoginRequest,
            crate::api::controllers::RegisterRequest,
            crate::api::controllers::TokenValidationRequest,
            crate::api::controllers::RefreshTokenRequest,
            crate::api::controllers::LogoutRequest,
            crate::api::controllers::AssignRolesRequest,
            crate::api::controllers::UpdateUserRequest,
            
            // Response schemas
            crate::api::controllers::LoginResponse,
            crate::api::controllers::TokenValidationResponse,
            crate::api::controllers::UserResponse,
            crate::api::controllers::RoleResponse,
            crate::api::controllers::PermissionResponse,
            crate::api::controllers::AssignRolesResponse,
            crate::api::controllers::CheckPermissionResponse,
            
            // Common schemas - use concrete type aliases instead of generic ApiResponse<T>
            crate::shared::types::ApiResponseString,
            crate::shared::types::ApiResponseLoginResponse,
            crate::shared::types::ApiResponseUserResponse,
            crate::shared::types::ApiResponseTokenValidationResponse,
            crate::shared::types::ApiResponseVecRoleResponse,
            crate::shared::types::ApiResponseVecPermissionResponse,
            crate::shared::types::ApiResponseAssignRolesResponse,
            crate::shared::types::ApiResponseCheckPermissionResponse,
            
            crate::shared::types::HealthCheckResponse,
            crate::shared::types::PaginationParams,
            crate::shared::types::PaginatedResponse<crate::api::controllers::UserResponse>,
            crate::shared::types::UserContext,
            crate::shared::types::SortParams,
            crate::shared::types::SortOrder,
            crate::shared::types::EmptyResponse,
            crate::shared::types::Id<String>,
        )
    ),
    tags(
        (name = "auth", description = "Authentication endpoints"),
        (name = "users", description = "User management endpoints"),
        (name = "system", description = "System endpoints")
    )
)]
pub struct ApiDoc;

// Fix the infinite recursion by calling the trait method
impl ApiDoc {
    pub fn openapi() -> utoipa::openapi::OpenApi {
        // Call the OpenApi trait's openapi method
        <Self as OpenApi>::openapi()
    }
}