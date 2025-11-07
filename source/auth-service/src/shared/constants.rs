// HTTP Headers
pub const AUTHORIZATION_HEADER: &str = "Authorization";
pub const BEARER_PREFIX: &str = "Bearer ";
pub const CONTENT_TYPE_JSON: &str = "application/json";

// Keycloak constants
pub const KEYCLOAK_TOKEN_ENDPOINT: &str = "protocol/openid-connect/token";
pub const KEYCLOAK_USERINFO_ENDPOINT: &str = "protocol/openid-connect/userinfo";
pub const KEYCLOAK_INTROSPECT_ENDPOINT: &str = "protocol/openid-connect/token/introspect";
pub const KEYCLOAK_LOGOUT_ENDPOINT: &str = "protocol/openid-connect/logout";

// Token constants
pub const ACCESS_TOKEN_TTL: i64 = 3600; // 1 hour in seconds
pub const REFRESH_TOKEN_TTL: i64 = 2592000; // 30 days in seconds

// Pagination constants
pub const DEFAULT_PAGE_SIZE: u32 = 20;
pub const MAX_PAGE_SIZE: u32 = 100;

// Validation constants
pub const MIN_PASSWORD_LENGTH: usize = 8;
pub const MAX_USERNAME_LENGTH: usize = 50;
pub const MAX_EMAIL_LENGTH: usize = 255;

// Cache constants
pub const DEFAULT_CACHE_TTL: u64 = 300; // 5 minutes in seconds
pub const TOKEN_CACHE_PREFIX: &str = "token:";
pub const USER_CACHE_PREFIX: &str = "user:";

// Role constants
pub const ROLE_USER: &str = "user";
pub const ROLE_ADMIN: &str = "admin";
pub const ROLE_SUPER_ADMIN: &str = "super_admin";

// Permission constants
pub const PERMISSION_READ: &str = "read";
pub const PERMISSION_WRITE: &str = "write";
pub const PERMISSION_DELETE: &str = "delete";
pub const PERMISSION_MANAGE_USERS: &str = "manage_users";

// API Route constants
pub const API_V1_PREFIX: &str = "/api/v1";
pub const HEALTH_CHECK_PATH: &str = "/health";
pub const LOGIN_PATH: &str = "/auth/login";
pub const REGISTER_PATH: &str = "/auth/register";
pub const VALIDATE_TOKEN_PATH: &str = "/auth/validate";
pub const REFRESH_TOKEN_PATH: &str = "/auth/refresh";
pub const LOGOUT_PATH: &str = "/auth/logout";