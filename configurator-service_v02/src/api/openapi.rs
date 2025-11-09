use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(
    paths(
        crate::api::health_routes::index,
        crate::api::health_routes::health_check,
        crate::api::health_routes::health_live,
        crate::api::health_routes::health_ready,
        crate::api::connector_type_handlers::list_connector_types,
        crate::api::connector_type_handlers::get_connector_type,
        crate::api::connector_type_handlers::create_connector_type,
        crate::api::connector_type_handlers::update_connector_type,
        crate::api::connector_type_handlers::delete_connector_type,
    ),
    components(
        schemas(
            crate::domain::connector_type_model::ConnectorType,
            crate::domain::connector_type_model::ConnectorTypeId,
            crate::application::connector_type_dto::ConnectorTypeDto,
            crate::application::connector_type_dto::CreateConnectorTypeDto,
            crate::application::connector_type_dto::UpdateConnectorTypeDto,
            crate::shared::errors::AppError,
            crate::shared::errors::ErrorType,
            crate::api::health_routes::HealthResponse,
            crate::api::health_routes::ServiceInfo,
            crate::api::health_routes::Endpoints,
        )
    ),
    tags(
        (name = "connector-types", description = "Connector Type management endpoints"),
        (name = "health", description = "Health check endpoints")
    ),
    info(
        title = "Configurator Service API",
        version = "1.0.0",
        description = "EV Charging Configurator Service with Connector Type management",
        contact(
            name = "API Support",
            email = "support@example.com"
        )
    )
)]
pub struct ApiDoc;

// Add the openapi method like in your working project
impl ApiDoc {
    pub fn openapi() -> utoipa::openapi::OpenApi {
        <Self as OpenApi>::openapi()
    }
}