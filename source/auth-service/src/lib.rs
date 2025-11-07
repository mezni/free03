// src/lib.rs
pub mod domain;
pub mod application;
pub mod infrastructure;
pub mod api;
pub mod shared;
pub mod config;
pub mod logger;

// Re-exports for convenient access
pub use config::Config;
pub use logger::init_logger;
pub use shared::error::AppError;
pub use shared::result::AppResult;

// Domain re-exports - rename AuthService to DomainAuthService to avoid conflict
pub use domain::{
    User, Role, Permission, Token, CreateUserRequest, TokenValidation,
    UserRepository, TokenRepository, RoleRepository, PermissionRepository, 
    AuthService as DomainAuthService  // Renamed here
};

// Application re-exports
pub use application::{
    AuthApplicationService,
    LoginCommand, RegisterCommand, AssignRolesCommand, ValidateTokenCommand,
    GetUserQuery, GetUserRolesQuery, CheckPermissionQuery,
    UserDto, TokenDto, LoginResponse, TokenValidationResponse
};

// Infrastructure re-exports
pub use infrastructure::KeycloakClient;

// API re-exports
pub use api::{
    configure_routes,
    LoginRequest, RegisterRequest, TokenValidationRequest,
    UserResponse, AssignRolesRequest
};

use std::sync::Arc;
use actix_web::{web, App, HttpServer};
use utoipa_swagger_ui::SwaggerUi;

// Type alias for easier usage - this is now unique
pub type AuthService = AuthApplicationService<KeycloakClient>;

#[derive(Clone)]
pub struct AppState {
    pub auth_service: Arc<AuthService>,
    pub config: Config,
}

impl AppState {
    pub fn new(
        auth_service: AuthService,
        config: Config,
    ) -> Self {
        Self {
            auth_service: Arc::new(auth_service),
            config,
        }
    }
}

pub struct Application {
    config: Config,
    app_state: AppState,
}

impl Application {
    pub async fn new() -> Result<Self, Box<dyn std::error::Error>> {
        // Load configuration
        let config = Config::from_env()?;

        // Initialize logging
        init_logger(&config.log)?;

        // Initialize Keycloak client
        let keycloak_client = KeycloakClient::new(
            config.keycloak.url.clone(),
            config.keycloak.realm.clone(),
            config.keycloak.client_id.clone(),
            config.keycloak.client_secret.clone(),
        );

        // Create application service
        let auth_service = AuthApplicationService::new(
            keycloak_client.clone(),
            keycloak_client.clone(),
            keycloak_client.clone(),
            keycloak_client,
        );

        let app_state = AppState::new(auth_service, config.clone());

        Ok(Self { config, app_state })
    }

    pub async fn run(self) -> std::io::Result<()> {
        tracing::info!("Starting auth service on {}", self.config.server_address());
        tracing::info!("Keycloak URL: {}", self.config.keycloak.url);
        tracing::info!("Keycloak Realm: {}", self.config.keycloak.realm);

        HttpServer::new(move || {
            App::new()
                .app_data(web::Data::new(self.app_state.clone()))
                .configure(api::configure_routes)
                .service(
                    SwaggerUi::new("/swagger-ui/{_:.*}")
                        .url("/api-docs/openapi.json", api::openapi::ApiDoc::openapi()),
                )
        })
        .bind(self.config.server_address())?
        .run()
        .await
    }
}