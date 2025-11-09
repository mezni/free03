use crate::domain::entities::stations::Point;
use crate::domain::entities::stations::Station;
use crate::domain::repositories::NetworkRepository;
use crate::domain::repositories::StationRepository;
use crate::shared::errors::AppError;
use async_trait::async_trait;
use std::collections::HashMap;
use uuid::Uuid;

pub struct CreateStationCommand {
    pub network_id: i32,
    pub name: String,
    pub address: String, // Required
    pub city: Option<String>,
    pub state: Option<String>,
    pub country: Option<String>,
    pub postal_code: Option<String>,
    pub location: Point,
    pub tags: Option<HashMap<String, String>>,
    pub osm_id: Option<i64>,
    pub is_operational: bool, // Required
    pub created_by: Uuid,     // Required
}

pub struct UpdateStationCommand {
    pub station_id: i32,
    pub name: Option<String>,
    pub address: Option<String>,
    pub city: Option<String>,
    pub state: Option<String>,
    pub country: Option<String>,
    pub postal_code: Option<String>,
    pub location: Option<Point>,
    pub tags: Option<HashMap<String, String>>,
    pub osm_id: Option<i64>,
    pub is_operational: Option<bool>,
    pub updated_by: Uuid, // Required
}

pub struct DeleteStationCommand {
    pub station_id: i32,
}

pub struct BulkCreateStationsCommand {
    pub network_id: i32,
    pub stations: Vec<CreateStationData>,
    pub created_by: Uuid, // Required
}

pub struct CreateStationData {
    pub name: String,
    pub address: String, // Required
    pub city: Option<String>,
    pub state: Option<String>,
    pub country: Option<String>,
    pub postal_code: Option<String>,
    pub location: Point,
    pub tags: Option<HashMap<String, String>>,
    pub osm_id: Option<i64>,
    pub is_operational: bool, // Required
}

#[async_trait]
pub trait StationCommandHandler: Send + Sync {
    async fn handle_create(&self, command: CreateStationCommand) -> Result<Station, AppError>;
    async fn handle_update(&self, command: UpdateStationCommand) -> Result<Station, AppError>;
    async fn handle_delete(&self, command: DeleteStationCommand) -> Result<(), AppError>;
    async fn handle_bulk_create(
        &self,
        command: BulkCreateStationsCommand,
    ) -> Result<Vec<Station>, AppError>;
}

pub struct StationCommandHandlerImpl {
    station_repository: Box<dyn StationRepository>,
    network_repository: Box<dyn NetworkRepository>,
}

impl StationCommandHandlerImpl {
    pub fn new(
        station_repository: Box<dyn StationRepository>,
        network_repository: Box<dyn NetworkRepository>,
    ) -> Self {
        Self {
            station_repository,
            network_repository,
        }
    }
}

#[async_trait]
impl StationCommandHandler for StationCommandHandlerImpl {
    async fn handle_create(&self, command: CreateStationCommand) -> Result<Station, AppError> {
        // Verify that the network exists
        let network = self
            .network_repository
            .find_by_id(command.network_id)
            .await?
            .ok_or_else(|| {
                AppError::NotFound(format!("Network with id {} not found", command.network_id))
            })?;

        // Check if station with same name already exists in this network
        let existing_stations = self
            .station_repository
            .find_by_network_id(command.network_id, 1, 10)
            .await?;

        if existing_stations.iter().any(|s| s.name == command.name) {
            return Err(AppError::Validation(format!(
                "Station with name '{}' already exists in this network",
                command.name
            )));
        }

        // Create new station entity
        let station = Station {
            station_id: 0, // Will be set by database
            network_id: command.network_id,
            name: command.name,
            address: command.address,
            city: command.city,
            state: command.state,
            country: command.country,
            postal_code: command.postal_code,
            location: command.location,
            tags: command.tags,
            osm_id: command.osm_id,
            is_operational: command.is_operational,
            created_by: command.created_by,
            updated_by: None,
            created_at: chrono::Utc::now(),
            updated_at: chrono::Utc::now(),
        };

        // Save to repository
        let saved_station = self.station_repository.save(&station).await?;

        Ok(saved_station)
    }

    async fn handle_update(&self, command: UpdateStationCommand) -> Result<Station, AppError> {
        // Find existing station
        let mut station = self
            .station_repository
            .find_by_id(command.station_id)
            .await?
            .ok_or_else(|| {
                AppError::NotFound(format!("Station with id {} not found", command.station_id))
            })?;

        // Check for name uniqueness if name is being updated
        if let Some(new_name) = &command.name {
            if &station.name != new_name {
                let existing_stations = self
                    .station_repository
                    .find_by_network_id(station.network_id, 1, 10)
                    .await?;

                if existing_stations.iter().any(|s| s.name == *new_name) {
                    return Err(AppError::Validation(format!(
                        "Station with name '{}' already exists in this network",
                        new_name
                    )));
                }
            }
        }

        // Update station fields
        if let Some(name) = command.name {
            station.name = name;
        }
        if let Some(address) = command.address {
            station.address = address;
        }
        if let Some(city) = command.city {
            station.city = Some(city);
        }
        if let Some(state) = command.state {
            station.state = Some(state);
        }
        if let Some(country) = command.country {
            station.country = Some(country);
        }
        if let Some(postal_code) = command.postal_code {
            station.postal_code = Some(postal_code);
        }
        if let Some(location) = command.location {
            station.location = location;
        }
        if let Some(tags) = command.tags {
            station.tags = Some(tags);
        }
        if let Some(osm_id) = command.osm_id {
            station.osm_id = Some(osm_id);
        }
        if let Some(is_operational) = command.is_operational {
            station.is_operational = is_operational;
        }

        station.updated_by = Some(command.updated_by);
        station.updated_at = chrono::Utc::now();

        // Save updated station
        let updated_station = self.station_repository.save(&station).await?;

        Ok(updated_station)
    }

    async fn handle_delete(&self, command: DeleteStationCommand) -> Result<(), AppError> {
        // Check if station exists
        let station = self
            .station_repository
            .find_by_id(command.station_id)
            .await?;

        if station.is_none() {
            return Err(AppError::NotFound(format!(
                "Station with id {} not found",
                command.station_id
            )));
        }

        // Delete station
        self.station_repository.delete(command.station_id).await?;

        Ok(())
    }

    async fn handle_bulk_create(
        &self,
        command: BulkCreateStationsCommand,
    ) -> Result<Vec<Station>, AppError> {
        // Verify that the network exists
        let network = self
            .network_repository
            .find_by_id(command.network_id)
            .await?
            .ok_or_else(|| {
                AppError::NotFound(format!("Network with id {} not found", command.network_id))
            })?;

        // Check for duplicate station names in the bulk request
        let mut station_names = std::collections::HashSet::new();
        for station_data in &command.stations {
            if !station_names.insert(&station_data.name) {
                return Err(AppError::Validation(format!(
                    "Duplicate station name '{}' in bulk create request",
                    station_data.name
                )));
            }
        }

        // Check if any stations already exist with these names
        let existing_stations = self
            .station_repository
            .find_by_network_id(command.network_id, 1, 1000)
            .await?;

        let existing_names: std::collections::HashSet<_> =
            existing_stations.iter().map(|s| &s.name).collect();

        for station_data in &command.stations {
            if existing_names.contains(&station_data.name) {
                return Err(AppError::Validation(format!(
                    "Station with name '{}' already exists in this network",
                    station_data.name
                )));
            }
        }

        // Create and save all stations
        let mut saved_stations = Vec::new();
        for station_data in command.stations {
            let station = Station {
                station_id: 0,
                network_id: command.network_id,
                name: station_data.name,
                address: station_data.address,
                city: station_data.city,
                state: station_data.state,
                country: station_data.country,
                postal_code: station_data.postal_code,
                location: station_data.location,
                tags: station_data.tags,
                osm_id: station_data.osm_id,
                is_operational: station_data.is_operational,
                created_by: command.created_by,
                updated_by: None,
                created_at: chrono::Utc::now(),
                updated_at: chrono::Utc::now(),
            };

            let saved_station = self.station_repository.save(&station).await?;
            saved_stations.push(saved_station);
        }

        Ok(saved_stations)
    }
}
