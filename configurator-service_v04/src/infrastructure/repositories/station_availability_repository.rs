use async_trait::async_trait;
use sqlx::PgPool;
use uuid::Uuid;
use chrono::NaiveTime;

use crate::domain::models::StationAvailability;
use crate::domain::repositories::{StationAvailabilityRepository, RepositoryResult, RepositoryError};
use crate::domain::value_objects::{StationId, UserId};

pub struct StationAvailabilityRepositoryImpl {
    pool: PgPool,
}

impl StationAvailabilityRepositoryImpl {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl StationAvailabilityRepository for StationAvailabilityRepositoryImpl {
    async fn find_by_id(&self, id: i32) -> RepositoryResult<Option<StationAvailability>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                availability_id, station_id, day_of_week, open_time, close_time,
                is_24_hours, created_by, updated_by, created_at, updated_at
            FROM station_availability 
            WHERE availability_id = $1
            "#,
            id
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                Ok(Some(StationAvailability {
                    id: record.availability_id,
                    station_id: StationId(record.station_id),
                    day_of_week: record.day_of_week,
                    open_time: record.open_time,
                    close_time: record.close_time,
                    is_24_hours: record.is_24_hours,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn find_by_station_id(&self, station_id: StationId) -> RepositoryResult<Vec<StationAvailability>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                availability_id, station_id, day_of_week, open_time, close_time,
                is_24_hours, created_by, updated_by, created_at, updated_at
            FROM station_availability
            WHERE station_id = $1
            ORDER BY day_of_week
            "#,
            station_id.0
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let availability_rules = records
            .into_iter()
            .map(|record| {
                StationAvailability {
                    id: record.availability_id,
                    station_id: StationId(record.station_id),
                    day_of_week: record.day_of_week,
                    open_time: record.open_time,
                    close_time: record.close_time,
                    is_24_hours: record.is_24_hours,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(availability_rules)
    }

    async fn save(&self, availability: &mut StationAvailability) -> RepositoryResult<()> {
        if availability.id == 0 {
            // Insert new availability rule
            let result = sqlx::query!(
                r#"
                INSERT INTO station_availability (
                    station_id, day_of_week, open_time, close_time,
                    is_24_hours, created_by, updated_by
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING availability_id, created_at, updated_at
                "#,
                availability.station_id.0,
                availability.day_of_week,
                availability.open_time,
                availability.close_time,
                availability.is_24_hours,
                Uuid::from(availability.created_by.0),
                availability.updated_by.map(|user_id| Uuid::from(user_id.0))
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            availability.id = result.availability_id;
            availability.created_at = result.created_at;
            availability.updated_at = result.updated_at;
        } else {
            // Update existing availability rule
            let result = sqlx::query!(
                r#"
                UPDATE station_availability 
                SET station_id = $1, day_of_week = $2, open_time = $3, close_time = $4,
                    is_24_hours = $5, updated_by = $6, updated_at = CURRENT_TIMESTAMP
                WHERE availability_id = $7
                RETURNING updated_at
                "#,
                availability.station_id.0,
                availability.day_of_week,
                availability.open_time,
                availability.close_time,
                availability.is_24_hours,
                availability.updated_by.map(|user_id| Uuid::from(user_id.0)),
                availability.id
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            availability.updated_at = result.updated_at;
        }

        Ok(())
    }

    async fn delete(&self, id: i32) -> RepositoryResult<()> {
        let rows_affected = sqlx::query!(
            "DELETE FROM station_availability WHERE availability_id = $1",
            id
        )
        .execute(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?
        .rows_affected();

        if rows_affected == 0 {
            return Err(RepositoryError::NotFound);
        }

        Ok(())
    }

    async fn delete_by_station_id(&self, station_id: StationId) -> RepositoryResult<()> {
        let rows_affected = sqlx::query!(
            "DELETE FROM station_availability WHERE station_id = $1",
            station_id.0
        )
        .execute(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?
        .rows_affected();

        if rows_affected == 0 {
            return Err(RepositoryError::NotFound);
        }

        Ok(())
    }
}

// Additional utility methods for station availability repository
impl StationAvailabilityRepositoryImpl {
    pub async fn find_availability_for_day(
        &self,
        station_id: StationId,
        day_of_week: i32,
    ) -> RepositoryResult<Option<StationAvailability>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                availability_id, station_id, day_of_week, open_time, close_time,
                is_24_hours, created_by, updated_by, created_at, updated_at
            FROM station_availability 
            WHERE station_id = $1 AND day_of_week = $2
            "#,
            station_id.0,
            day_of_week
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                Ok(Some(StationAvailability {
                    id: record.availability_id,
                    station_id: StationId(record.station_id),
                    day_of_week: record.day_of_week,
                    open_time: record.open_time,
                    close_time: record.close_time,
                    is_24_hours: record.is_24_hours,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    pub async fn find_24_7_stations(&self) -> RepositoryResult<Vec<StationId>> {
        let records = sqlx::query!(
            r#"
            SELECT DISTINCT station_id
            FROM station_availability
            WHERE is_24_hours = true
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let station_ids = records
            .into_iter()
            .map(|record| StationId(record.station_id))
            .collect();

        Ok(station_ids)
    }

    pub async fn is_station_open_at_time(
        &self,
        station_id: StationId,
        day_of_week: i32,
        current_time: NaiveTime,
    ) -> RepositoryResult<bool> {
        let result = sqlx::query!(
            r#"
            SELECT 
                is_24_hours,
                open_time,
                close_time
            FROM station_availability 
            WHERE station_id = $1 AND day_of_week = $2
            "#,
            station_id.0,
            day_of_week
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                if record.is_24_hours {
                    // Station is open 24/7 on this day
                    Ok(true)
                } else if let (Some(open_time), Some(close_time)) = (record.open_time, record.close_time) {
                    // Check if current time is within opening hours
                    if open_time <= close_time {
                        // Normal time window (e.g., 08:00-20:00)
                        Ok(current_time >= open_time && current_time <= close_time)
                    } else {
                        // Overnight time window (e.g., 20:00-08:00)
                        Ok(current_time >= open_time || current_time <= close_time)
                    }
                } else {
                    // Invalid time configuration
                    Ok(false)
                }
            }
            None => {
                // No availability rule for this day, assume closed
                Ok(false)
            }
        }
    }

    pub async fn get_stations_open_at_time(
        &self,
        day_of_week: i32,
        current_time: NaiveTime,
    ) -> RepositoryResult<Vec<StationId>> {
        let records = sqlx::query!(
            r#"
            SELECT DISTINCT station_id
            FROM station_availability
            WHERE day_of_week = $1
            AND (
                is_24_hours = true OR
                (
                    open_time IS NOT NULL AND 
                    close_time IS NOT NULL AND
                    (
                        (open_time <= close_time AND $2 BETWEEN open_time AND close_time) OR
                        (open_time > close_time AND ($2 >= open_time OR $2 <= close_time))
                    )
                )
            )
            "#,
            day_of_week,
            current_time
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let station_ids = records
            .into_iter()
            .map(|record| StationId(record.station_id))
            .collect();

        Ok(station_ids)
    }

    pub async fn bulk_insert_availability(
        &self,
        availability_rules: &[StationAvailability],
        created_by: UserId,
    ) -> RepositoryResult<()> {
        if availability_rules.is_empty() {
            return Ok(());
        }

        let mut transaction = self.pool.begin().await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        for availability in availability_rules {
            sqlx::query!(
                r#"
                INSERT INTO station_availability (
                    station_id, day_of_week, open_time, close_time,
                    is_24_hours, created_by
                )
                VALUES ($1, $2, $3, $4, $5, $6)
                "#,
                availability.station_id.0,
                availability.day_of_week,
                availability.open_time,
                availability.close_time,
                availability.is_24_hours,
                Uuid::from(created_by.0)
            )
            .execute(&mut *transaction)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;
        }

        transaction.commit().await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        Ok(())
    }

    pub async fn update_station_availability(
        &self,
        station_id: StationId,
        availability_rules: Vec<StationAvailability>,
        updated_by: UserId,
    ) -> RepositoryResult<()> {
        let mut transaction = self.pool.begin().await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        // Delete existing availability rules for this station
        sqlx::query!(
            "DELETE FROM station_availability WHERE station_id = $1",
            station_id.0
        )
        .execute(&mut *transaction)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        // Insert new availability rules
        for availability in availability_rules {
            sqlx::query!(
                r#"
                INSERT INTO station_availability (
                    station_id, day_of_week, open_time, close_time,
                    is_24_hours, created_by, updated_by
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                "#,
                availability.station_id.0,
                availability.day_of_week,
                availability.open_time,
                availability.close_time,
                availability.is_24_hours,
                Uuid::from(availability.created_by.0),
                Uuid::from(updated_by.0)
            )
            .execute(&mut *transaction)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;
        }

        transaction.commit().await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        Ok(())
    }

    pub async fn find_stations_with_complete_schedule(&self) -> RepositoryResult<Vec<StationId>> {
        let records = sqlx::query!(
            r#"
            SELECT station_id, COUNT(*) as rule_count
            FROM station_availability
            GROUP BY station_id
            HAVING COUNT(*) = 7  -- All 7 days of the week
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let station_ids = records
            .into_iter()
            .map(|record| StationId(record.station_id))
            .collect();

        Ok(station_ids)
    }

    pub async fn find_stations_with_partial_schedule(&self) -> RepositoryResult<Vec<StationId>> {
        let records = sqlx::query!(
            r#"
            SELECT station_id, COUNT(*) as rule_count
            FROM station_availability
            GROUP BY station_id
            HAVING COUNT(*) > 0 AND COUNT(*) < 7  -- Some but not all days
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let station_ids = records
            .into_iter()
            .map(|record| StationId(record.station_id))
            .collect();

        Ok(station_ids)
    }

    pub async fn find_stations_without_schedule(&self) -> RepositoryResult<Vec<StationId>> {
        let records = sqlx::query!(
            r#"
            SELECT s.station_id
            FROM stations s
            LEFT JOIN station_availability sa ON s.station_id = sa.station_id
            WHERE sa.availability_id IS NULL
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let station_ids = records
            .into_iter()
            .map(|record| StationId(record.station_id))
            .collect();

        Ok(station_ids)
    }

    pub async fn get_station_operating_hours_summary(
        &self,
        station_id: StationId,
    ) -> RepositoryResult<StationOperatingHoursSummary> {
        let records = sqlx::query!(
            r#"
            SELECT 
                day_of_week,
                is_24_hours,
                open_time,
                close_time
            FROM station_availability
            WHERE station_id = $1
            ORDER BY day_of_week
            "#,
            station_id.0
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let mut days_24_7 = 0;
        let mut days_with_hours = 0;
        let mut days_closed = 7; // Start with all days closed

        for record in &records {
            days_closed -= 1; // Each record represents one day that's not completely closed
            
            if record.is_24_hours {
                days_24_7 += 1;
            } else if record.open_time.is_some() && record.close_time.is_some() {
                days_with_hours += 1;
            }
        }

        Ok(StationOperatingHoursSummary {
            station_id,
            total_days_configured: records.len() as u32,
            days_24_7,
            days_with_specific_hours: days_with_hours,
            days_closed,
        })
    }
}

#[derive(Debug, Clone)]
pub struct StationOperatingHoursSummary {
    pub station_id: StationId,
    pub total_days_configured: u32,
    pub days_24_7: u32,
    pub days_with_specific_hours: u32,
    pub days_closed: u32,
}

#[derive(Debug, Clone)]
pub struct StationOpenStatus {
    pub station_id: StationId,
    pub is_open: bool,
    pub next_opening_time: Option<NaiveTime>,
    pub next_opening_day: Option<i32>,
}