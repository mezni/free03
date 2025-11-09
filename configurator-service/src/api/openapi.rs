use utoipa::OpenApi;

#[derive(OpenApi)]
#[openapi(
    paths(
        // Network endpoints
        crate::api::handlers::networks::create_network,
        crate::api::handlers::networks::get_network,
        crate::api::handlers::networks::list_networks,
        crate::api::handlers::networks::update_network,
        crate::api::handlers::networks::delete_network,
        // Company endpoints  
        crate::api::handlers::companies::create_company,
        crate::api::handlers::companies::get_company,
        crate::api::handlers::companies::get_company_by_network,
        crate::api::handlers::companies::update_company,
        crate::api::handlers::companies::delete_company,
        // Station endpoints
        crate::api::handlers::stations::create_station,
        crate::api::handlers::stations::get_station,
        crate::api::handlers::stations::get_stations_by_network,
        crate::api::handlers::stations::get_operational_stations,
        crate::api::handlers::stations::update_station,
        crate::api::handlers::stations::delete_station,
        crate::api::handlers::stations::search_stations,
    ),
    components(
        schemas(
            // Network schemas
            crate::api::dtos::networks::CreateNetworkRequest,
            crate::api::dtos::networks::UpdateNetworkRequest,
            crate::api::dtos::networks::NetworkResponse,
            crate::api::dtos::networks::NetworkListResponse,
            // Company schemas
            crate::api::dtos::companies::CreateCompanyRequest,
            crate::api::dtos::companies::UpdateCompanyRequest,
            crate::api::dtos::companies::CompanyResponse,
            // Station schemas
            crate::api::dtos::stations::CreateStationRequest,
            crate::api::dtos::stations::UpdateStationRequest,
            crate::api::dtos::stations::StationResponse,
            crate::api::dtos::stations::StationsResponse,
            crate::api::dtos::points::PointDto,
            // Error schema
            crate::shared::errors::AppError,
        )
    ),
    tags(
        (name = "Networks", description = "Network management endpoints"),
        (name = "Companies", description = "Company management endpoints"),
        (name = "Stations", description = "Station management endpoints")
    )
)]
pub struct ApiDoc;
