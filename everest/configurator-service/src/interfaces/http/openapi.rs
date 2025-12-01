use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(
    paths(
        crate::application::handlers::health::health_checker_handler,
        crate::application::handlers::user::get_users_handler,
        crate::application::handlers::user::get_user_handler,
        crate::application::handlers::user::create_user_handler
    ),
    components(
        schemas(
            crate::application::dtos::health::HealthResponse,
            crate::application::dtos::user::User,
            crate::application::dtos::user::CreateUserRequest,
            crate::application::dtos::user::UserResponse,
            crate::application::dtos::user::ErrorResponse
        )
    ),
    tags(
        (name = "Configurator Service", description = "Manage resources")
    )
)]
pub struct ApiDoc;
