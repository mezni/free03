use super::models::{Station, Connector};
use super::value_objects::*;
use super::events::{DomainEvent, StationCreated, ConnectorStatusChanged};
use super::traits::{AggregateRoot, EventProducer};
use chrono::Utc;

// Station Aggregate Root
pub struct StationAggregate {
    station: Station,
    connectors: Vec<Connector>,
    events: Vec<DomainEvent>,
}

impl StationAggregate {
    pub fn new(
        network_id: NetworkId,
        name: String,
        address: String,
        location: Location,
        created_by: UserId,
    ) -> Result<Self, &'static str> {
        let station = Station::new(
            network_id,
            name,
            address,
            None, // city
            None, // state
            None, // country
            None, // postal_code
            location,
            Default::default(), // tags
            None, // osm_id
            created_by,
        )?;

        let mut aggregate = Self {
            station,
            connectors: Vec::new(),
            events: Vec::new(),
        };

        // Add domain event
        aggregate.add_domain_event(DomainEvent::StationCreated(StationCreated {
            station_id: aggregate.station.id,
            network_id,
            name: aggregate.station.name.clone(),
            location: aggregate.station.location.clone(),
            created_by,
            occurred_at: Utc::now(),
        }));

        Ok(aggregate)
    }

    pub fn add_connector(
        &mut self,
        connector_type_id: ConnectorTypeId,
        power_level_kw: PowerKW,
        created_by: UserId,
    ) -> Result<ConnectorId, &'static str> {
        let connector = Connector::new(
            self.station.id,
            connector_type_id,
            power_level_kw,
            None, // max_voltage
            None, // max_amperage
            None, // serial_number
            None, // manufacturer
            None, // model
            None, // installation_date
            created_by,
        );

        let connector_id = connector.id;
        self.connectors.push(connector);

        Ok(connector_id)
    }

    pub fn update_connector_status(
        &mut self,
        connector_id: ConnectorId,
        new_status: ConnectorStatus,
        updated_by: UserId,
    ) -> Result<(), &'static str> {
        let connector = self.connectors
            .iter_mut()
            .find(|c| c.id == connector_id)
            .ok_or("Connector not found in station")?;

        let old_status = connector.status.clone();
        connector.update_status(new_status.clone(), updated_by);

        // Add domain event
        self.add_domain_event(DomainEvent::ConnectorStatusChanged(
            super::events::ConnectorStatusChanged {
                connector_id,
                station_id: self.station.id,
                old_status,
                new_status,
                changed_by: updated_by,
                occurred_at: Utc::now(),
            }
        ));

        Ok(())
    }

    pub fn station(&self) -> &Station {
        &self.station
    }

    pub fn connectors(&self) -> &[Connector] {
        &self.connectors
    }

    pub fn available_connectors(&self) -> Vec<&Connector> {
        self.connectors
            .iter()
            .filter(|c| c.is_available())
            .collect()
    }
}

impl AggregateRoot for StationAggregate {
    type Id = StationId;
}

impl Entity<StationId> for StationAggregate {
    fn id(&self) -> StationId {
        self.station.id
    }
}

impl EventProducer for StationAggregate {
    fn domain_events(&self) -> &[DomainEvent] {
        &self.events
    }

    fn add_domain_event(&mut self, event: DomainEvent) {
        self.events.push(event);
    }

    fn clear_domain_events(&mut self) {
        self.events.clear();
    }
}