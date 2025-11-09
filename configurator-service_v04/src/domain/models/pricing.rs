use super::super::value_objects::*;
use chrono::{DateTime, Utc, NaiveDate};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Pricing {
    pub id: i32,
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
    pub is_active: bool,
    pub effective_from: NaiveDate,
    pub effective_until: Option<NaiveDate>,
    pub created_by: UserId,
    pub updated_by: Option<UserId>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl Pricing {
    pub fn new(
        network_id: NetworkId,
        connector_type_id: Option<ConnectorTypeId>,
        pricing_model: PricingModel,
        cost_per_kwh: Option<f64>,
        cost_per_minute: Option<f64>,
        flat_rate_cost: Option<f64>,
        membership_fee: Option<f64>,
        start_time: Option<chrono::NaiveTime>,
        end_time: Option<chrono::NaiveTime>,
        day_of_week: Option<i32>,
        effective_from: NaiveDate,
        effective_until: Option<NaiveDate>,
        created_by: UserId,
    ) -> Result<Self, &'static str> {
        if effective_from < NaiveDate::from_ymd_opt(2020, 1, 1).unwrap() {
            return Err("Effective from date cannot be before 2020");
        }

        if let Some(effective_until) = effective_until {
            if effective_until <= effective_from {
                return Err("Effective until must be after effective from");
            }
        }

        let now = Utc::now();
        Ok(Self {
            id: 0, // Will be set by repository
            network_id,
            connector_type_id,
            pricing_model,
            cost_per_kwh,
            cost_per_minute,
            flat_rate_cost,
            membership_fee,
            start_time,
            end_time,
            day_of_week,
            is_active: true,
            effective_from,
            effective_until,
            created_by,
            updated_by: None,
            created_at: now,
            updated_at: now,
        })
    }

    pub fn deactivate(&mut self, updated_by: UserId) {
        self.is_active = false;
        self.updated_by = Some(updated_by);
        self.updated_at = Utc::now();
    }

    pub fn is_currently_effective(&self, date: NaiveDate) -> bool {
        if !self.is_active {
            return false;
        }

        if date < self.effective_from {
            return false;
        }

        if let Some(effective_until) = self.effective_until {
            if date > effective_until {
                return false;
            }
        }

        true
    }
}