use utoipa::OpenApi;
use crate::api::handlers::{
    connector_status_handler,
    connector_type_handler,
    station_handler,
};

#[derive(OpenApi)]
#[openapi(
    paths(
        connector_status_handler::get_connector_statuses,
        connector_status_handler::create_connector_status,
        connector_type_handler::get_all_connector_types,
        connector_type_handler::create_connector_type,
        station_handler::get_all_stations,
        station_handler::create_station
    ),
    components(
        schemas(
            connector_status_handler::ConnectorStatusDTO,
            connector_status_handler::CreateConnectorStatusDTO,
            connector_type_handler::ConnectorTypeDTO,
            connector_type_handler::CreateConnectorTypeDTO,
            station_handler::StationDTO,
            station_handler::CreateStationDTO
        )
    ),
    tags(
        (name = "ConnectorStatus", description = "Manage connector status"),
        (name = "ConnectorTypes", description = "Manage connector types"),
        (name = "Stations", description = "Manage EV stations")
    )
)]
pub struct ApiDoc;
