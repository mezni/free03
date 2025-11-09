use serde::{Deserialize, Serialize};
use utoipa::{ToSchema, IntoParams};

use crate::domain::value_objects::{NetworkId, ConnectorTypeId, PricingModel};

// ===== REQUESTS =====

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct CreatePricingRuleRequest {
    pub network_id: NetworkId,
    pub connector_type_id: Option<ConnectorTypeId>,
    pub pricing_model: PricingModel,
    #[schema(example = 0.30)]
    pub cost_per_kwh: Option<f64>,
    #[schema(example = 0.10)]
    pub cost_per_minute: Option<f64>,
    #[schema(example = 5.00)]
    pub flat_rate_cost: Option<f64>,
    #[schema(example = 29.99)]
    pub membership_fee: Option<f64>,
    pub start_time: Option<chrono::NaiveTime>,
    pub end_time: Option<chrono::NaiveTime>,
    pub day_of_week: Option<i32>,
    pub effective_from: chrono::NaiveDate,
    pub effective_until: Option<chrono::NaiveDate>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct UpdatePricingRuleRequest {
    #[schema(example = 0.35)]
    pub cost_per_kwh: Option<f64>,
    #[schema(example = 0.12)]
    pub cost_per_minute: Option<f64>,
    #[schema(example = 6.00)]
    pub flat_rate_cost: Option<f64>,
    #[schema(example = 39.99)]
    pub membership_fee: Option<f64>,
    pub start_time: Option<chrono::NaiveTime>,
    pub end_time: Option<chrono::NaiveTime>,
    pub day_of_week: Option<i32>,
    pub effective_until: Option<chrono::NaiveDate>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct CalculateCostRequest {
    pub network_id: NetworkId,
    pub connector_type_id: Option<ConnectorTypeId>,
    pub pricing_model: PricingModel,
    pub energy_kwh: Option<f64>,
    pub duration_minutes: Option<i64>,
    pub date: chrono::NaiveDate,
    pub time: Option<chrono::NaiveTime>,
}

#[derive(Debug, Deserialize, IntoParams)]
pub struct ListPricingRulesParams {
    pub network_id: i32,
    #[param(example = 1)]
    pub page: Option<u32>,
    #[param(example = 20)]
    pub page_size: Option<u32>,
    pub active_only: Option<bool>,
}

#[derive(Debug, Deserialize, IntoParams)]
pub struct PricingHistoryParams {
    pub network_id: i32,
    pub start_date: chrono::NaiveDate,
    pub end_date: chrono::NaiveDate,
}

// ===== RESPONSES =====

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct PricingRuleResponse {
    pub pricing_id: i32,
    pub network_id: i32,
    pub connector_type: Option<crate::api::dtos::connectors::ConnectorTypeResponse>,
    pub pricing_model: PricingModel,
    pub cost_per_kwh: Option<f64>,
    pub cost_per_minute: Option<f64>,
    pub flat_rate_cost: Option<f64>,
    pub membership_fee: Option<f64>,
    pub start_time: Option<String>,
    pub end_time: Option<String>,
    pub day_of_week: Option<i32>,
    pub is_active: bool,
    pub effective_from: String,
    pub effective_until: Option<String>,
    pub created_at: String,
    pub updated_at: String,
}

impl PricingRuleResponse {
    pub fn from_dto(dto: crate::application::queries::pricing_queries::PricingRuleDto) -> Self {
        Self {
            pricing_id: dto.pricing_id,
            network_id: dto.network_id,
            connector_type: dto.connector_type.map(crate::api::dtos::connectors::ConnectorTypeResponse::from_dto),
            pricing_model: dto.pricing_model,
            cost_per_kwh: dto.cost_per_kwh,
            cost_per_minute: dto.cost_per_minute,
            flat_rate_cost: dto.flat_rate_cost,
            membership_fee: dto.membership_fee,
            start_time: dto.start_time.map(|t| t.to_string()),
            end_time: dto.end_time.map(|t| t.to_string()),
            day_of_week: dto.day_of_week,
            is_active: dto.is_active,
            effective_from: dto.effective_from.to_string(),
            effective_until: dto.effective_until.map(|d| d.to_string()),
            created_at: dto.created_at.to_rfc3339(),
            updated_at: dto.updated_at.to_rfc3339(),
        }
    }
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct PricingRuleListResponse {
    pub pricing_rules: Vec<PricingRuleResponse>,
    pub total_count: u64,
    pub page: u32,
    pub page_size: u32,
    pub total_pages: u32,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct CostCalculationResponse {
    pub network_id: i32,
    pub connector_type_id: Option<i32>,
    pub pricing_model: PricingModel,
    pub energy_kwh: Option<f64>,
    pub duration_minutes: Option<i64>,
    pub calculated_cost: f64,
    pub currency: String,
    pub applicable_pricing_rules: Vec<PricingRuleResponse>,
}

#[derive(Debug, Deserialize, Serialize, ToSchema)]
pub struct PricingHistoryResponse {
    pub pricing_rules: Vec<PricingRuleResponse>,
    pub total_count: u64,
}