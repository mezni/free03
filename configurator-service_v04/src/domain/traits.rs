use async_trait::async_trait;
use super::value_objects::*;
use super::events::DomainEvent;

// Trait for entities that can produce domain events
pub trait EventProducer {
    fn domain_events(&self) -> &[DomainEvent];
    fn add_domain_event(&mut self, event: DomainEvent);
    fn clear_domain_events(&mut self);
}

// Trait for entities that have an identity
pub trait Entity<T>: EventProducer {
    fn id(&self) -> T;
}

// Trait for aggregate roots
pub trait AggregateRoot: Entity<<Self as AggregateRoot>::Id> {
    type Id;
}

// Trait for value objects
pub trait ValueObject: Clone + PartialEq {
    fn validate(&self) -> Result<(), &'static str>;
}

// Trait for domain services
#[async_trait]
pub trait DomainService: Send + Sync {
    async fn execute(&self) -> Result<(), Box<dyn std::error::Error>>;
}

// Trait for specifications (query specifications)
pub trait Specification<T> {
    fn is_satisfied_by(&self, candidate: &T) -> bool;
}

// Example specification for available stations
pub struct OperationalStationSpec;

impl Specification<super::models::Station> for OperationalStationSpec {
    fn is_satisfied_by(&self, station: &super::models::Station) -> bool {
        station.is_operational
    }
}

// Example specification for available connectors
pub struct AvailableConnectorSpec;

impl Specification<super::models::Connector> for AvailableConnectorSpec {
    fn is_satisfied_by(&self, connector: &super::models::Connector) -> bool {
        connector.is_available()
    }
}