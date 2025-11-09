use serde::{Deserialize, Serialize};
use uuid::Uuid;
use std::str::FromStr;

// External User ID from authentication server
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct UserId(pub Uuid);

impl UserId {
    pub fn new(id: Uuid) -> Self {
        Self(id)
    }
    
    pub fn parse_str(s: &str) -> Result<Self, uuid::Error> {
        Ok(Self(Uuid::parse_str(s)?))
    }
}

impl From<Uuid> for UserId {
    fn from(uuid: Uuid) -> Self {
        Self(uuid)
    }
}

// Network ID
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct NetworkId(pub i32);

impl NetworkId {
    pub fn new(id: i32) -> Self {
        Self(id)
    }
}

// Station ID
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct StationId(pub i32);

impl StationId {
    pub fn new(id: i32) -> Self {
        Self(id)
    }
}

// Connector ID
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct ConnectorId(pub i32);

impl ConnectorId {
    pub fn new(id: i32) -> Self {
        Self(id)
    }
}

// Connector Type ID
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct ConnectorTypeId(pub i32);

impl ConnectorTypeId {
    pub fn new(id: i32) -> Self {
        Self(id)
    }
}

// Charging Session ID
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct ChargingSessionId(pub i32);

impl ChargingSessionId {
    pub fn new(id: i32) -> Self {
        Self(id)
    }
}

// Geographic Location
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub struct Location {
    pub latitude: f64,
    pub longitude: f64,
}

impl Location {
    pub fn new(latitude: f64, longitude: f64) -> Result<Self, &'static str> {
        if !(-90.0..=90.0).contains(&latitude) {
            return Err("Latitude must be between -90 and 90");
        }
        if !(-180.0..=180.0).contains(&longitude) {
            return Err("Longitude must be between -180 and 180");
        }
        Ok(Self { latitude, longitude })
    }
}

// Power in kilowatts
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct PowerKW(pub f64);

impl PowerKW {
    pub fn new(power: f64) -> Result<Self, &'static str> {
        if power < 0.0 {
            return Err("Power cannot be negative");
        }
        Ok(Self(power))
    }
}

// Energy in kilowatt-hours
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct EnergyKWH(pub f64);

impl EnergyKWH {
    pub fn new(energy: f64) -> Result<Self, &'static str> {
        if energy < 0.0 {
            return Err("Energy cannot be negative");
        }
        Ok(Self(energy))
    }
}

// Money value
#[derive(Debug, Clone, Copy, PartialEq, Serialize, Deserialize)]
pub struct Money {
    pub amount: f64,
    pub currency: String, // ISO 4217 code
}

impl Money {
    pub fn new(amount: f64, currency: &str) -> Result<Self, &'static str> {
        if amount < 0.0 {
            return Err("Money amount cannot be negative");
        }
        if currency.len() != 3 {
            return Err("Currency must be 3 characters (ISO 4217)");
        }
        Ok(Self {
            amount,
            currency: currency.to_uppercase(),
        })
    }
}

// Network Type
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum NetworkType {
    Individual,
    Company,
}

// Connector Current Type
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum CurrentType {
    AC,
    DC,
}

// Connector Status
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum ConnectorStatus {
    Available,
    Occupied,
    OutOfService,
    Reserved,
}

// Charging Session Status
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum ChargingSessionStatus {
    Active,
    Completed,
    Cancelled,
    Interrupted,
}

// Payment Status
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum PaymentStatus {
    Pending,
    Paid,
    Failed,
    Refunded,
}

// Pricing Model
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum PricingModel {
    PerKWH,
    PerMinute,
    FlatRate,
    Membership,
}

// Company Size
#[derive(Debug, Clone, PartialEq, Serialize, Deserialize)]
pub enum CompanySize {
    Small,
    Medium,
    Large,
}

// OSM ID
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct OsmId(pub i64);

impl OsmId {
    pub fn new(id: i64) -> Self {
        Self(id)
    }
}

// Tags as key-value pairs
pub type Tags = std::collections::HashMap<String, String>;