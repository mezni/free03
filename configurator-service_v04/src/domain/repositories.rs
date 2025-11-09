use async_trait::async_trait;
use crate::domain::models::*;
use crate::domain::value_objects::*;

// Result type for repository operations
pub type RepositoryResult<T> = Result<T, RepositoryError>;

#[derive(Debug, thiserror::Error)]
pub enum RepositoryError {
    #[error("Entity not found")]
    NotFound,
    #[error("Database error: {0}")]
    DatabaseError(String),
    #[error("Constraint violation: {0}")]
    ConstraintViolation(String),
    #[error("Connection error: {0}")]
    ConnectionError(String),
}

#[async_trait]
pub trait NetworkRepository: Send + Sync {
    async fn find_by_id(&self, id: NetworkId) -> RepositoryResult<Option<Network>>;
    async fn find_by_name(&self, name: &str) -> RepositoryResult<Option<Network>>;
    async fn save(&self, network: &mut Network) -> RepositoryResult<()>;
    async fn delete(&self, id: NetworkId) -> RepositoryResult<()>;
    async fn find_all(&self) -> RepositoryResult<Vec<Network>>;
    async fn find_by_type(&self, network_type: NetworkType) -> RepositoryResult<Vec<Network>>;
}

#[async_trait]
pub trait CompanyRepository: Send + Sync {
    async fn find_by_id(&self, id: i32) -> RepositoryResult<Option<Company>>;
    async fn find_by_network_id(&self, network_id: NetworkId) -> RepositoryResult<Option<Company>>;
    async fn save(&self, company: &mut Company) -> RepositoryResult<()>;
    async fn delete(&self, id: i32) -> RepositoryResult<()>;
}

#[async_trait]
pub trait StationRepository: Send + Sync {
    async fn find_by_id(&self, id: StationId) -> RepositoryResult<Option<Station>>;
    async fn find_by_network_id(&self, network_id: NetworkId) -> RepositoryResult<Vec<Station>>;
    async fn find_by_location(
        &self,
        latitude: f64,
        longitude: f64,
        radius_km: f64,
    ) -> RepositoryResult<Vec<Station>>;
    async fn find_by_osm_id(&self, osm_id: OsmId) -> RepositoryResult<Option<Station>>;
    async fn save(&self, station: &mut Station) -> RepositoryResult<()>;
    async fn delete(&self, id: StationId) -> RepositoryResult<()>;
    async fn find_operational_stations(&self) -> RepositoryResult<Vec<Station>>;
}

#[async_trait]
pub trait ConnectorTypeRepository: Send + Sync {
    async fn find_by_id(&self, id: ConnectorTypeId) -> RepositoryResult<Option<ConnectorType>>;
    async fn find_by_name(&self, name: &str) -> RepositoryResult<Option<ConnectorType>>;
    async fn find_by_current_type(&self, current_type: CurrentType) -> RepositoryResult<Vec<ConnectorType>>;
    async fn save(&self, connector_type: &mut ConnectorType) -> RepositoryResult<()>;
    async fn delete(&self, id: ConnectorTypeId) -> RepositoryResult<()>;
    async fn find_all(&self) -> RepositoryResult<Vec<ConnectorType>>;
}

#[async_trait]
pub trait ConnectorRepository: Send + Sync {
    async fn find_by_id(&self, id: ConnectorId) -> RepositoryResult<Option<Connector>>;
    async fn find_by_station_id(&self, station_id: StationId) -> RepositoryResult<Vec<Connector>>;
    async fn find_available_by_station_id(&self, station_id: StationId) -> RepositoryResult<Vec<Connector>>;
    async fn find_by_status(&self, status: ConnectorStatus) -> RepositoryResult<Vec<Connector>>;
    async fn save(&self, connector: &mut Connector) -> RepositoryResult<()>;
    async fn delete(&self, id: ConnectorId) -> RepositoryResult<()>;
}

#[async_trait]
pub trait ChargingSessionRepository: Send + Sync {
    async fn find_by_id(&self, id: ChargingSessionId) -> RepositoryResult<Option<ChargingSession>>;
    async fn find_by_user_id(&self, user_id: UserId) -> RepositoryResult<Vec<ChargingSession>>;
    async fn find_by_connector_id(&self, connector_id: ConnectorId) -> RepositoryResult<Vec<ChargingSession>>;
    async fn find_active_sessions(&self) -> RepositoryResult<Vec<ChargingSession>>;
    async fn find_sessions_in_date_range(
        &self,
        start_date: chrono::DateTime<Utc>,
        end_date: chrono::DateTime<Utc>,
    ) -> RepositoryResult<Vec<ChargingSession>>;
    async fn save(&self, session: &mut ChargingSession) -> RepositoryResult<()>;
    async fn delete(&self, id: ChargingSessionId) -> RepositoryResult<()>;
}

#[async_trait]
pub trait PricingRepository: Send + Sync {
    async fn find_by_id(&self, id: i32) -> RepositoryResult<Option<Pricing>>;
    async fn find_by_network_id(&self, network_id: NetworkId) -> RepositoryResult<Vec<Pricing>>;
    async fn find_active_pricing_for_network(
        &self,
        network_id: NetworkId,
        connector_type_id: Option<ConnectorTypeId>,
        date: chrono::NaiveDate,
    ) -> RepositoryResult<Vec<Pricing>>;
    async fn save(&self, pricing: &mut Pricing) -> RepositoryResult<()>;
    async fn delete(&self, id: i32) -> RepositoryResult<()>;
}

#[async_trait]
pub trait StationAvailabilityRepository: Send + Sync {
    async fn find_by_id(&self, id: i32) -> RepositoryResult<Option<StationAvailability>>;
    async fn find_by_station_id(&self, station_id: StationId) -> RepositoryResult<Vec<StationAvailability>>;
    async fn save(&self, availability: &mut StationAvailability) -> RepositoryResult<()>;
    async fn delete(&self, id: i32) -> RepositoryResult<()>;
    async fn delete_by_station_id(&self, station_id: StationId) -> RepositoryResult<()>;
}

// Repository trait that aggregates all repositories
pub trait RepositoryCollection: Send + Sync {
    fn networks(&self) -> &dyn NetworkRepository;
    fn companies(&self) -> &dyn CompanyRepository;
    fn stations(&self) -> &dyn StationRepository;
    fn connector_types(&self) -> &dyn ConnectorTypeRepository;
    fn connectors(&self) -> &dyn ConnectorRepository;
    fn charging_sessions(&self) -> &dyn ChargingSessionRepository;
    fn pricing(&self) -> &dyn PricingRepository;
    fn station_availability(&self) -> &dyn StationAvailabilityRepository;
}