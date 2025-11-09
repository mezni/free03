use serde::{Deserialize, Serialize};

use crate::domain::value_objects::{NetworkId, ConnectorTypeId, PricingModel, UserId};

// Command to create a pricing rule
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CreatePricingRuleCommand {
    pub network_id: NetworkId,
    pub connector_type_id: Option<ConnectorTypeId>,
    pub pricing_model: PricingModel,
    pub cost_per_kwh: Option<f64>,
    pub cost_per_minute: Option<f64>,
    pub flat_rate_cost: Option<f64>,
    pub membership_fee: Option<f64>,
    pub start_time: Option<chrono::NaiveTime>,
    pub end_time: Option<chrono::NaiveTime>,
    pub day_of_week: Option<i32>,
    pub effective_from: chrono::NaiveDate,
    pub effective_until: Option<chrono::NaiveDate>,
    pub created_by: UserId,
}

// Command to update a pricing rule
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct UpdatePricingRuleCommand {
    pub pricing_id: i32,
    pub cost_per_kwh: Option<f64>,
    pub cost_per_minute: Option<f64>,
    pub flat_rate_cost: Option<f64>,
    pub membership_fee: Option<f64>,
    pub start_time: Option<chrono::NaiveTime>,
    pub end_time: Option<chrono::NaiveTime>,
    pub day_of_week: Option<i32>,
    pub effective_until: Option<chrono::NaiveDate>,
    pub updated_by: UserId,
}

// Command to deactivate a pricing rule
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeactivatePricingRuleCommand {
    pub pricing_id: i32,
    pub deactivated_by: UserId,
}

// Command to delete a pricing rule
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DeletePricingRuleCommand {
    pub pricing_id: i32,
    pub deleted_by: UserId,
}

// Command to calculate cost for a session
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CalculateCostCommand {
    pub network_id: NetworkId,
    pub connector_type_id: Option<ConnectorTypeId>,
    pub pricing_model: PricingModel,
    pub energy_kwh: Option<f64>,
    pub duration_minutes: Option<i64>,
    pub date: chrono::NaiveDate,
    pub time: Option<chrono::NaiveTime>,
}