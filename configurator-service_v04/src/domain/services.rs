use crate::domain::models::*;
use crate::domain::repositories::*;
use crate::domain::value_objects::*;

pub struct StationManagementService {
    station_repo: Box<dyn StationRepository>,
    connector_repo: Box<dyn ConnectorRepository>,
}

impl StationManagementService {
    pub fn new(
        station_repo: Box<dyn StationRepository>,
        connector_repo: Box<dyn ConnectorRepository>,
    ) -> Self {
        Self {
            station_repo,
            connector_repo,
        }
    }

    pub async fn create_station_with_connectors(
        &self,
        network_id: NetworkId,
        name: String,
        address: String,
        location: Location,
        created_by: UserId,
        connectors: Vec<(ConnectorTypeId, PowerKW)>,
    ) -> Result<StationId, &'static str> {
        // Create station
        let mut station = Station::new(
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

        // Save station to get ID
        self.station_repo.save(&mut station).await
            .map_err(|_| "Failed to save station")?;

        // Create connectors
        for (connector_type_id, power_level) in connectors {
            let mut connector = Connector::new(
                station.id,
                connector_type_id,
                power_level,
                None, // max_voltage
                None, // max_amperage
                None, // serial_number
                None, // manufacturer
                None, // model
                None, // installation_date
                created_by,
            );

            self.connector_repo.save(&mut connector).await
                .map_err(|_| "Failed to save connector")?;
        }

        Ok(station.id)
    }
}

pub struct ChargingSessionService {
    session_repo: Box<dyn ChargingSessionRepository>,
    connector_repo: Box<dyn ConnectorRepository>,
    pricing_repo: Box<dyn PricingRepository>,
}

impl ChargingSessionService {
    pub fn new(
        session_repo: Box<dyn ChargingSessionRepository>,
        connector_repo: Box<dyn ConnectorRepository>,
        pricing_repo: Box<dyn PricingRepository>,
    ) -> Self {
        Self {
            session_repo,
            connector_repo,
            pricing_repo,
        }
    }

    pub async fn start_charging_session(
        &self,
        connector_id: ConnectorId,
        user_id: UserId,
        payment_method: Option<String>,
    ) -> Result<ChargingSessionId, &'static str> {
        // Check if connector exists and is available
        let connector = self.connector_repo.find_by_id(connector_id).await
            .map_err(|_| "Failed to fetch connector")?
            .ok_or("Connector not found")?;

        if !connector.is_available() {
            return Err("Connector is not available");
        }

        // Create charging session
        let mut session = ChargingSession::new(
            connector_id,
            user_id,
            payment_method,
            user_id, // initiated_by same as user_id
        );

        // Save session
        self.session_repo.save(&mut session).await
            .map_err(|_| "Failed to save charging session")?;

        // Update connector status
        // Note: In a real implementation, you'd need mutable access to connector
        // This would require a more sophisticated approach with transactions

        Ok(session.id)
    }

    pub async fn calculate_session_cost(
        &self,
        session_id: ChargingSessionId,
        energy_used: EnergyKWH,
        duration_minutes: i64,
    ) -> Result<Money, &'static str> {
        let session = self.session_repo.find_by_id(session_id).await
            .map_err(|_| "Failed to fetch session")?
            .ok_or("Session not found")?;

        let connector = self.connector_repo.find_by_id(session.connector_id).await
            .map_err(|_| "Failed to fetch connector")?
            .ok_or("Connector not found")?;

        // Get pricing for the connector's network and type
        let pricing_rules = self.pricing_repo
            .find_active_pricing_for_network(
                // This would need to be fetched from station -> network
                // For simplicity, we're assuming we have network_id
                NetworkId(1), // This should come from the connector's station
                Some(connector.connector_type_id),
                chrono::Utc::now().date_naive(),
            )
            .await
            .map_err(|_| "Failed to fetch pricing")?;

        if pricing_rules.is_empty() {
            return Err("No pricing rules found");
        }

        // Simple cost calculation - use the first pricing rule
        let pricing = &pricing_rules[0];
        let cost = match pricing.pricing_model {
            PricingModel::PerKWH => {
                pricing.cost_per_kwh.unwrap_or(0.0) * energy_used.0
            }
            PricingModel::PerMinute => {
                pricing.cost_per_minute.unwrap_or(0.0) * duration_minutes as f64
            }
            PricingModel::FlatRate => {
                pricing.flat_rate_cost.unwrap_or(0.0)
            }
            PricingModel::Membership => {
                pricing.membership_fee.unwrap_or(0.0)
            }
        };

        Money::new(cost, "USD").map_err(|_| "Invalid cost calculation")
    }
}