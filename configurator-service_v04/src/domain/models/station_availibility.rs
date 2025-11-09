use super::super::value_objects::*;
use chrono::{DateTime, Utc};
use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct StationAvailability {
    pub id: i32,
    pub station_id: StationId,
    pub day_of_week: i32, // 0=Sunday, 6=Saturday
    pub open_time: Option<chrono::NaiveTime>,
    pub close_time: Option<chrono::NaiveTime>,
    pub is_24_hours: bool,
    pub created_by: UserId,
    pub updated_by: Option<UserId>,
    pub created_at: DateTime<Utc>,
    pub updated_at: DateTime<Utc>,
}

impl StationAvailability {
    pub fn new(
        station_id: StationId,
        day_of_week: i32,
        open_time: Option<chrono::NaiveTime>,
        close_time: Option<chrono::NaiveTime>,
        is_24_hours: bool,
        created_by: UserId,
    ) -> Result<Self, &'static str> {
        if !(0..=6).contains(&day_of_week) {
            return Err("Day of week must be between 0 (Sunday) and 6 (Saturday)");
        }

        if is_24_hours && (open_time.is_some() || close_time.is_some()) {
            return Err("24-hour stations cannot have open/close times");
        }

        if !is_24_hours && (open_time.is_none() || close_time.is_none()) {
            return Err("Non-24-hour stations must have both open and close times");
        }

        let now = Utc::now();
        Ok(Self {
            id: 0, // Will be set by repository
            station_id,
            day_of_week,
            open_time,
            close_time,
            is_24_hours,
            created_by,
            updated_by: None,
            created_at: now,
            updated_at: now,
        })
    }
}