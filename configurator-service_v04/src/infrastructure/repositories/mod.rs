pub mod network_repository;
pub mod company_repository;
pub mod station_repository;
pub mod connector_type_repository;
pub mod connector_repository;
pub mod charging_session_repository;
pub mod pricing_repository;
pub mod station_availability_repository;

// Re-export all repositories
pub use network_repository::*;
pub use company_repository::*;
pub use station_repository::*;
pub use connector_type_repository::*;
pub use connector_repository::*;
pub use charging_session_repository::*;
pub use pricing_repository::*;
pub use station_availability_repository::*;

use sqlx::PgPool;
use crate::domain::repositories::*;

// Repository collection implementation
pub struct SqlxRepositoryCollection {
    network_repo: NetworkRepositoryImpl,
    company_repo: CompanyRepositoryImpl,
    station_repo: StationRepositoryImpl,
    connector_type_repo: ConnectorTypeRepositoryImpl,
    connector_repo: ConnectorRepositoryImpl,
    charging_session_repo: ChargingSessionRepositoryImpl,
    pricing_repo: PricingRepositoryImpl,
    station_availability_repo: StationAvailabilityRepositoryImpl,
}

impl SqlxRepositoryCollection {
    pub fn new(pool: PgPool) -> Self {
        Self {
            network_repo: NetworkRepositoryImpl::new(pool.clone()),
            company_repo: CompanyRepositoryImpl::new(pool.clone()),
            station_repo: StationRepositoryImpl::new(pool.clone()),
            connector_type_repo: ConnectorTypeRepositoryImpl::new(pool.clone()),
            connector_repo: ConnectorRepositoryImpl::new(pool.clone()),
            charging_session_repo: ChargingSessionRepositoryImpl::new(pool.clone()),
            pricing_repo: PricingRepositoryImpl::new(pool.clone()),
            station_availability_repo: StationAvailabilityRepositoryImpl::new(pool),
        }
    }
}

impl RepositoryCollection for SqlxRepositoryCollection {
    fn networks(&self) -> &dyn NetworkRepository {
        &self.network_repo
    }

    fn companies(&self) -> &dyn CompanyRepository {
        &self.company_repo
    }

    fn stations(&self) -> &dyn StationRepository {
        &self.station_repo
    }

    fn connector_types(&self) -> &dyn ConnectorTypeRepository {
        &self.connector_type_repo
    }

    fn connectors(&self) -> &dyn ConnectorRepository {
        &self.connector_repo
    }

    fn charging_sessions(&self) -> &dyn ChargingSessionRepository {
        &self.charging_session_repo
    }

    fn pricing(&self) -> &dyn PricingRepository {
        &self.pricing_repo
    }

    fn station_availability(&self) -> &dyn StationAvailabilityRepository {
        &self.station_availability_repo
    }
}