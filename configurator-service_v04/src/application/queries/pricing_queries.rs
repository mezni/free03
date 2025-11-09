use serde::{Deserialize, Serialize};

use crate::domain::value_objects::{NetworkId, ConnectorTypeId, PricingModel};

// Query to get pricing rule by ID
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetPricingRuleByIdQuery {
    pub pricing_id: i32,
}

// Query to list pricing rules by network
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ListPricingRulesByNetworkQuery {
    pub network_id: NetworkId,
    pub page: Option<u32>,
    pub page_size: Option<u32>,
}

// Query to get active pricing for network
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetActivePricingForNetworkQuery {
    pub network_id: NetworkId,
    pub connector_type_id: Option<ConnectorTypeId>,
    pub date: chrono::NaiveDate,
}

// Query to calculate cost
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CalculateCostQuery {
    pub network_id: NetworkId,
    pub connector_type_id: Option<ConnectorTypeId>,
    pub pricing_model: PricingModel,
    pub energy_kwh: Option<f64>,
    pub duration_minutes: Option<i64>,
    pub date: chrono::NaiveDate,
    pub time: Option<chrono::NaiveTime>,
}

// Query to get pricing history
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GetPricingHistoryQuery {
    pub network_id: NetworkId,
    pub start_date: chrono::NaiveDate,
    pub end_date: chrono::NaiveDate,
}

// Query results
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PricingRuleDto {
    pub pricing_id: i32,
    pub network_id: i32,
    pub connector_type: Option<crate::application::queries::connector_queries::ConnectorTypeDto>,
    pub pricing_model: PricingModel,
    pub cost_per_kwh: Option<f64>,
    pub cost_per_minute: Option<f64>,
    pub flat_rate_cost: Option<f64>,
    pub membership_fee: Option<f64>,
    pub start_time: Option<chrono::NaiveTime>,
    pub end_time: Option<chrono::NaiveTime>,
    pub day_of_week: Option<i32>,
    pub is_active: bool,
    pub effective_from: chrono::NaiveDate,
    pub effective_until: Option<chrono::NaiveDate>,
    pub created_at: chrono::DateTime<chrono::Utc>,
    pub updated_at: chrono::DateTime<chrono::Utc>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CostCalculationDto {
    pub network_id: i32,
    pub connector_type_id: Option<i32>,
    pub pricing_model: PricingModel,
    pub energy_kwh: Option<f64>,
    pub duration_minutes: Option<i64>,
    pub calculated_cost: f64,
    pub currency: String,
    pub applicable_pricing_rules: Vec<PricingRuleDto>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PricingRuleListResponse {
    pub pricing_rules: Vec<PricingRuleDto>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PricingHistoryResponse {
    pub pricing_rules: Vec<PricingRuleDto>,
    pub total_count: u64,
}