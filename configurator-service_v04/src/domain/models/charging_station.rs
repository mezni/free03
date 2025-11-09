use super::super::value_objects::*;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ChargingSession {
    pub id: ChargingSessionId,
    pub connector_id: ConnectorId,
    pub user_id: UserId,
    pub start_time: DateTime<Utc>,
    pub end_time: Option<DateTime<Utc>>,
    pub energy_delivered_kwh: Option<EnergyKWH>,
    pub total_cost: Option<Money>,
    pub payment_status: PaymentStatus,
    pub payment_method: Option<String>,
    pub session_status: ChargingSessionStatus,
    pub initiated_by: UserId,
    pub ended_by: Option<UserId>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl ChargingSession {
    pub fn new(
        connector_id: ConnectorId,
        user_id: UserId,
        payment_method: Option<String>,
        initiated_by: UserId,
    ) -> Self {
        let now = Utc::now();
        Self {
            id: ChargingSessionId(0), // Will be set by repository
            connector_id,
            user_id,
            start_time: now,
            end_time: None,
            energy_delivered_kwh: None,
            total_cost: None,
            payment_status: PaymentStatus::Pending,
            payment_method,
            session_status: ChargingSessionStatus::Active,
            initiated_by,
            ended_by: None,
            created_at: now,
            updated_at: now,
        }
    }

    pub fn complete(
        &mut self,
        end_time: DateTime<Utc>,
        energy_delivered_kwh: EnergyKWH,
        total_cost: Money,
        ended_by: UserId,
    ) -> Result<(), &'static str> {
        if end_time <= self.start_time {
            return Err("End time must be after start time");
        }

        self.end_time = Some(end_time);
        self.energy_delivered_kwh = Some(energy_delivered_kwh);
        self.total_cost = Some(total_cost);
        self.session_status = ChargingSessionStatus::Completed;
        self.ended_by = Some(ended_by);
        self.updated_at = Utc::now();

        Ok(())
    }

    pub fn cancel(&mut self, ended_by: UserId) {
        self.end_time = Some(Utc::now());
        self.session_status = ChargingSessionStatus::Cancelled;
        self.ended_by = Some(ended_by);
        self.updated_at = Utc::now();
    }

    pub fn mark_paid(&mut self) {
        self.payment_status = PaymentStatus::Paid;
        self.updated_at = Utc::now();
    }

    pub fn duration_minutes(&self) -> Option<i64> {
        self.end_time.map(|end| {
            let duration = end - self.start_time;
            duration.num_minutes()
        })
    }

    pub fn is_active(&self) -> bool {
        matches!(self.session_status, ChargingSessionStatus::Active)
    }
}