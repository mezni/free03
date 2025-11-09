use crate::domain::entities::stations::Station;
use crate::domain::repositories::StationRepository;
use crate::shared::errors::AppError;
use async_trait::async_trait;

pub struct GetStationQuery {
    pub station_id: i32,
}

pub struct GetStationsByNetworkQuery {
    pub network_id: i32,
    pub page: u32,
    pub page_size: u32,
}

pub struct GetOperationalStationsQuery {
    pub network_id: i32,
}

pub struct SearchStationsQuery {
    pub network_id: Option<i32>,
    pub name: Option<String>,
    pub city: Option<String>,
    pub country: Option<String>,
    pub is_operational: Option<bool>,
    pub page: u32,
    pub page_size: u32,
}

pub struct StationsResponse {
    pub stations: Vec<Station>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
}

pub struct StationResponse {
    pub station: Station,
}

#[async_trait]
pub trait StationQueryHandler: Send + Sync {
    async fn handle_get(&self, query: GetStationQuery) -> Result<StationResponse, AppError>;
    async fn handle_get_by_network(
        &self,
        query: GetStationsByNetworkQuery,
    ) -> Result<StationsResponse, AppError>;
    async fn handle_get_operational(
        &self,
        query: GetOperationalStationsQuery,
    ) -> Result<StationsResponse, AppError>;
    async fn handle_search(&self, query: SearchStationsQuery)
    -> Result<StationsResponse, AppError>;
}

pub struct StationQueryHandlerImpl {
    station_repository: Box<dyn StationRepository>,
}

impl StationQueryHandlerImpl {
    pub fn new(station_repository: Box<dyn StationRepository>) -> Self {
        Self { station_repository }
    }
}

#[async_trait]
impl StationQueryHandler for StationQueryHandlerImpl {
    async fn handle_get(&self, query: GetStationQuery) -> Result<StationResponse, AppError> {
        let station = self
            .station_repository
            .find_by_id(query.station_id)
            .await?
            .ok_or_else(|| {
                AppError::NotFound(format!("Station with id {} not found", query.station_id))
            })?;

        Ok(StationResponse { station })
    }

    async fn handle_get_by_network(
        &self,
        query: GetStationsByNetworkQuery,
    ) -> Result<StationsResponse, AppError> {
        let stations = self
            .station_repository
            .find_by_network_id(query.network_id, query.page, query.page_size)
            .await?;

        // Note: For proper pagination, you might want to add a count method to your repository
        // For now, we'll use the length as total_count
        let total_count = stations.len() as u64;

        Ok(StationsResponse {
            stations,
            total_count,
            page: query.page,
            page_size: query.page_size,
        })
    }

    async fn handle_get_operational(
        &self,
        query: GetOperationalStationsQuery,
    ) -> Result<StationsResponse, AppError> {
        let stations = self
            .station_repository
            .find_operational_by_network(query.network_id)
            .await?;

        let total_count = stations.len() as u64;

        Ok(StationsResponse {
            stations,
            total_count,
            page: 1,
            page_size: total_count as u32,
        })
    }

    async fn handle_search(
        &self,
        query: SearchStationsQuery,
    ) -> Result<StationsResponse, AppError> {
        // For now, we'll implement a basic search using existing repository methods
        // In a real application, you might want to add a dedicated search method to the repository

        let mut all_stations = Vec::new();

        if let Some(network_id) = query.network_id {
            // If network_id is specified, get stations from that network
            let stations = self
                .station_repository
                .find_by_network_id(network_id, 1, 1000) // Use large page size for search
                .await?;
            all_stations.extend(stations);
        } else {
            // If no network specified, this would need a different repository method
            // For now, we'll return an empty result or implement getAll method
            return Err(AppError::Validation(
                "Search across all networks not implemented yet".to_string(),
            ));
        }

        // Apply filters
        let filtered_stations: Vec<Station> = all_stations
            .into_iter()
            .filter(|station| {
                // Filter by name (case insensitive partial match)
                if let Some(ref name_filter) = query.name {
                    if !station
                        .name
                        .to_lowercase()
                        .contains(&name_filter.to_lowercase())
                    {
                        return false;
                    }
                }

                // Filter by city
                if let Some(ref city_filter) = query.city {
                    match &station.city {
                        Some(city) if city.to_lowercase().contains(&city_filter.to_lowercase()) => {
                        }
                        Some(_) => return false,
                        None => return false,
                    }
                }

                // Filter by country
                if let Some(ref country_filter) = query.country {
                    match &station.country {
                        Some(country)
                            if country
                                .to_lowercase()
                                .contains(&country_filter.to_lowercase()) => {}
                        Some(_) => return false,
                        None => return false,
                    }
                }

                // Filter by operational status
                if let Some(is_operational_filter) = query.is_operational {
                    if station.is_operational != is_operational_filter {
                        return false;
                    }
                }

                true
            })
            .collect();

        // Apply pagination
        let total_count = filtered_stations.len() as u64;
        let start_index = ((query.page - 1) * query.page_size) as usize;
        let end_index = std::cmp::min(
            start_index + query.page_size as usize,
            filtered_stations.len(),
        );

        let paginated_stations = if start_index < filtered_stations.len() {
            filtered_stations[start_index..end_index].to_vec()
        } else {
            Vec::new()
        };

        Ok(StationsResponse {
            stations: paginated_stations,
            total_count,
            page: query.page,
            page_size: query.page_size,
        })
    }
}
