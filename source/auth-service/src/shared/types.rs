use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::marker::PhantomData;
use utoipa::ToSchema;

/// Generic response wrapper for API responses
#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct ApiResponse<T> {
    pub success: bool,
    pub data: T,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub message: Option<String>,
}

impl<T> ApiResponse<T> {
    pub fn new(data: T) -> Self {
        Self {
            success: true,
            data,
            message: None,
        }
    }

    pub fn with_message(data: T, message: &str) -> Self {
        Self {
            success: true,
            data,
            message: Some(message.to_string()),
        }
    }
}

// Concrete type aliases for OpenAPI schema generation
pub type ApiResponseString = ApiResponse<String>;
pub type ApiResponseLoginResponse = ApiResponse<crate::api::controllers::LoginResponse>;
pub type ApiResponseUserResponse = ApiResponse<crate::api::controllers::UserResponse>;
pub type ApiResponseTokenValidationResponse = ApiResponse<crate::api::controllers::TokenValidationResponse>;
pub type ApiResponseVecRoleResponse = ApiResponse<Vec<crate::api::controllers::RoleResponse>>;
pub type ApiResponseVecPermissionResponse = ApiResponse<Vec<crate::api::controllers::PermissionResponse>>;
pub type ApiResponseAssignRolesResponse = ApiResponse<crate::api::controllers::AssignRolesResponse>;
pub type ApiResponseCheckPermissionResponse = ApiResponse<crate::api::controllers::CheckPermissionResponse>;

/// Pagination parameters
#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct PaginationParams {
    pub page: Option<u32>,
    pub size: Option<u32>,
}

impl Default for PaginationParams {
    fn default() -> Self {
        Self {
            page: Some(1),
            size: Some(20),
        }
    }
}

/// Paginated response
#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct PaginatedResponse<T> {
    pub items: Vec<T>,
    pub total: u64,
    pub page: u32,
    pub size: u32,
    pub total_pages: u32,
}

impl<T> PaginatedResponse<T> {
    pub fn new(items: Vec<T>, total: u64, page: u32, size: u32) -> Self {
        let total_pages = ((total as f64) / (size as f64)).ceil() as u32;
        Self {
            items,
            total,
            page,
            size,
            total_pages,
        }
    }
}

/// Health check response
#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct HealthCheckResponse {
    pub status: String,
    pub timestamp: String,
    pub version: String,
    pub dependencies: HashMap<String, String>,
}

impl Default for HealthCheckResponse {
    fn default() -> Self {
        Self {
            status: "healthy".to_string(),
            timestamp: chrono::Utc::now().to_rfc3339(),
            version: env!("CARGO_PKG_VERSION").to_string(),
            dependencies: HashMap::new(),
        }
    }
}

/// User context for request processing
#[derive(Debug, Clone, Serialize, Deserialize, ToSchema)]
pub struct UserContext {
    pub user_id: String,
    pub username: String,
    pub email: String,
    pub roles: Vec<String>,
    pub permissions: Vec<String>,
}

impl UserContext {
    pub fn new(user_id: String, username: String, email: String) -> Self {
        Self {
            user_id,
            username,
            email,
            roles: Vec::new(),
            permissions: Vec::new(),
        }
    }

    pub fn has_role(&self, role: &str) -> bool {
        self.roles.iter().any(|r| r == role)
    }

    pub fn has_permission(&self, permission: &str) -> bool {
        self.permissions.iter().any(|p| p == permission)
    }

    pub fn is_admin(&self) -> bool {
        self.has_role("admin") || self.has_role("super_admin")
    }
}

/// Sorting parameters
#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct SortParams {
    pub sort_by: Option<String>,
    pub sort_order: Option<SortOrder>,
}

#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub enum SortOrder {
    Asc,
    Desc,
}

impl Default for SortOrder {
    fn default() -> Self {
        Self::Asc
    }
}

/// Empty response for operations that don't return data
#[derive(Debug, Serialize, Deserialize, ToSchema)]
pub struct EmptyResponse;

/// ID wrapper for type-safe IDs
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash, ToSchema)]
pub struct Id<T>(
    pub String, 
    #[serde(skip, default = "PhantomData::default")] 
    PhantomData<T>
);

impl<T> Id<T> {
    pub fn new(id: String) -> Self {
        Self(id, PhantomData)
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
    
    pub fn into_inner(self) -> String {
        self.0
    }
}

impl<T> std::fmt::Display for Id<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.0)
    }
}

// Implement From<String> for convenience
impl<T> From<String> for Id<T> {
    fn from(value: String) -> Self {
        Self::new(value)
    }
}

// Implement From<&str> for convenience
impl<T> From<&str> for Id<T> {
    fn from(value: &str) -> Self {
        Self::new(value.to_string())
    }
}