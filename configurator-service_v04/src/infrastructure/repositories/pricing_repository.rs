use async_trait::async_trait;
use sqlx::PgPool;
use uuid::Uuid;
use chrono::{NaiveDate, NaiveTime};

use crate::domain::models::Pricing;
use crate::domain::repositories::{PricingRepository, RepositoryResult, RepositoryError};
use crate::domain::value_objects::{NetworkId, ConnectorTypeId, PricingModel, UserId};

pub struct PricingRepositoryImpl {
    pool: PgPool,
}

impl PricingRepositoryImpl {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl PricingRepository for PricingRepositoryImpl {
    async fn find_by_id(&self, id: i32) -> RepositoryResult<Option<Pricing>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                pricing_id, network_id, connector_type_id,
                pricing_model as "pricing_model!: String",
                cost_per_kwh, cost_per_minute, flat_rate_cost, membership_fee,
                start_time, end_time, day_of_week,
                is_active, effective_from, effective_until,
                created_by, updated_by, created_at, updated_at
            FROM pricing 
            WHERE pricing_id = $1
            "#,
            id
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let pricing_model = match record.pricing_model.as_str() {
                    "per_kwh" => PricingModel::PerKWH,
                    "per_minute" => PricingModel::PerMinute,
                    "flat_rate" => PricingModel::FlatRate,
                    "membership" => PricingModel::Membership,
                    _ => return Err(RepositoryError::DatabaseError("Invalid pricing model".to_string())),
                };

                Ok(Some(Pricing {
                    id: record.pricing_id,
                    network_id: NetworkId(record.network_id),
                    connector_type_id: record.connector_type_id.map(ConnectorTypeId),
                    pricing_model,
                    cost_per_kwh: record.cost_per_kwh,
                    cost_per_minute: record.cost_per_minute,
                    flat_rate_cost: record.flat_rate_cost,
                    membership_fee: record.membership_fee,
                    start_time: record.start_time,
                    end_time: record.end_time,
                    day_of_week: record.day_of_week,
                    is_active: record.is_active,
                    effective_from: record.effective_from,
                    effective_until: record.effective_until,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn find_by_network_id(&self, network_id: NetworkId) -> RepositoryResult<Vec<Pricing>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                pricing_id, network_id, connector_type_id,
                pricing_model as "pricing_model!: String",
                cost_per_kwh, cost_per_minute, flat_rate_cost, membership_fee,
                start_time, end_time, day_of_week,
                is_active, effective_from, effective_until,
                created_by, updated_by, created_at, updated_at
            FROM pricing
            WHERE network_id = $1
            ORDER BY effective_from DESC, pricing_id
            "#,
            network_id.0
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let pricing_rules = records
            .into_iter()
            .map(|record| {
                let pricing_model = match record.pricing_model.as_str() {
                    "per_kwh" => PricingModel::PerKWH,
                    "per_minute" => PricingModel::PerMinute,
                    "flat_rate" => PricingModel::FlatRate,
                    "membership" => PricingModel::Membership,
                    _ => panic!("Invalid pricing model in database"),
                };

                Pricing {
                    id: record.pricing_id,
                    network_id: NetworkId(record.network_id),
                    connector_type_id: record.connector_type_id.map(ConnectorTypeId),
                    pricing_model,
                    cost_per_kwh: record.cost_per_kwh,
                    cost_per_minute: record.cost_per_minute,
                    flat_rate_cost: record.flat_rate_cost,
                    membership_fee: record.membership_fee,
                    start_time: record.start_time,
                    end_time: record.end_time,
                    day_of_week: record.day_of_week,
                    is_active: record.is_active,
                    effective_from: record.effective_from,
                    effective_until: record.effective_until,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(pricing_rules)
    }

    async fn find_active_pricing_for_network(
        &self,
        network_id: NetworkId,
        connector_type_id: Option<ConnectorTypeId>,
        date: NaiveDate,
    ) -> RepositoryResult<Vec<Pricing>> {
        let connector_type_id_value = connector_type_id.map(|id| id.0);

        let records = sqlx::query!(
            r#"
            SELECT 
                pricing_id, network_id, connector_type_id,
                pricing_model as "pricing_model!: String",
                cost_per_kwh, cost_per_minute, flat_rate_cost, membership_fee,
                start_time, end_time, day_of_week,
                is_active, effective_from, effective_until,
                created_by, updated_by, created_at, updated_at
            FROM pricing
            WHERE network_id = $1
            AND (connector_type_id = $2 OR connector_type_id IS NULL)
            AND is_active = true
            AND effective_from <= $3
            AND (effective_until IS NULL OR effective_until >= $3)
            ORDER BY 
                connector_type_id NULLS LAST, -- Prefer connector-specific pricing over general
                day_of_week NULLS LAST, -- Prefer day-specific pricing
                start_time NULLS LAST -- Prefer time-specific pricing
            "#,
            network_id.0,
            connector_type_id_value,
            date
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let pricing_rules = records
            .into_iter()
            .map(|record| {
                let pricing_model = match record.pricing_model.as_str() {
                    "per_kwh" => PricingModel::PerKWH,
                    "per_minute" => PricingModel::PerMinute,
                    "flat_rate" => PricingModel::FlatRate,
                    "membership" => PricingModel::Membership,
                    _ => panic!("Invalid pricing model in database"),
                };

                Pricing {
                    id: record.pricing_id,
                    network_id: NetworkId(record.network_id),
                    connector_type_id: record.connector_type_id.map(ConnectorTypeId),
                    pricing_model,
                    cost_per_kwh: record.cost_per_kwh,
                    cost_per_minute: record.cost_per_minute,
                    flat_rate_cost: record.flat_rate_cost,
                    membership_fee: record.membership_fee,
                    start_time: record.start_time,
                    end_time: record.end_time,
                    day_of_week: record.day_of_week,
                    is_active: record.is_active,
                    effective_from: record.effective_from,
                    effective_until: record.effective_until,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(pricing_rules)
    }

    async fn save(&self, pricing: &mut Pricing) -> RepositoryResult<()> {
        let pricing_model_str = match pricing.pricing_model {
            PricingModel::PerKWH => "per_kwh",
            PricingModel::PerMinute => "per_minute",
            PricingModel::FlatRate => "flat_rate",
            PricingModel::Membership => "membership",
        };

        if pricing.id == 0 {
            // Insert new pricing rule
            let result = sqlx::query!(
                r#"
                INSERT INTO pricing (
                    network_id, connector_type_id, pricing_model,
                    cost_per_kwh, cost_per_minute, flat_rate_cost, membership_fee,
                    start_time, end_time, day_of_week,
                    is_active, effective_from, effective_until,
                    created_by, updated_by
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
                RETURNING pricing_id, created_at, updated_at
                "#,
                pricing.network_id.0,
                pricing.connector_type_id.map(|id| id.0),
                pricing_model_str,
                pricing.cost_per_kwh,
                pricing.cost_per_minute,
                pricing.flat_rate_cost,
                pricing.membership_fee,
                pricing.start_time,
                pricing.end_time,
                pricing.day_of_week,
                pricing.is_active,
                pricing.effective_from,
                pricing.effective_until,
                Uuid::from(pricing.created_by.0),
                pricing.updated_by.map(|user_id| Uuid::from(user_id.0))
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            pricing.id = result.pricing_id;
            pricing.created_at = result.created_at;
            pricing.updated_at = result.updated_at;
        } else {
            // Update existing pricing rule
            let result = sqlx::query!(
                r#"
                UPDATE pricing 
                SET network_id = $1, connector_type_id = $2, pricing_model = $3,
                    cost_per_kwh = $4, cost_per_minute = $5, flat_rate_cost = $6, membership_fee = $7,
                    start_time = $8, end_time = $9, day_of_week = $10,
                    is_active = $11, effective_from = $12, effective_until = $13,
                    updated_by = $14, updated_at = CURRENT_TIMESTAMP
                WHERE pricing_id = $15
                RETURNING updated_at
                "#,
                pricing.network_id.0,
                pricing.connector_type_id.map(|id| id.0),
                pricing_model_str,
                pricing.cost_per_kwh,
                pricing.cost_per_minute,
                pricing.flat_rate_cost,
                pricing.membership_fee,
                pricing.start_time,
                pricing.end_time,
                pricing.day_of_week,
                pricing.is_active,
                pricing.effective_from,
                pricing.effective_until,
                pricing.updated_by.map(|user_id| Uuid::from(user_id.0)),
                pricing.id
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            pricing.updated_at = result.updated_at;
        }

        Ok(())
    }

    async fn delete(&self, id: i32) -> RepositoryResult<()> {
        let rows_affected = sqlx::query!(
            "DELETE FROM pricing WHERE pricing_id = $1",
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
}

// Additional utility methods for pricing repository
impl PricingRepositoryImpl {
    pub async fn find_by_connector_type_id(
        &self, 
        connector_type_id: ConnectorTypeId
    ) -> RepositoryResult<Vec<Pricing>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                pricing_id, network_id, connector_type_id,
                pricing_model as "pricing_model!: String",
                cost_per_kwh, cost_per_minute, flat_rate_cost, membership_fee,
                start_time, end_time, day_of_week,
                is_active, effective_from, effective_until,
                created_by, updated_by, created_at, updated_at
            FROM pricing
            WHERE connector_type_id = $1
            ORDER BY effective_from DESC, pricing_id
            "#,
            connector_type_id.0
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let pricing_rules = records
            .into_iter()
            .map(|record| {
                let pricing_model = match record.pricing_model.as_str() {
                    "per_kwh" => PricingModel::PerKWH,
                    "per_minute" => PricingModel::PerMinute,
                    "flat_rate" => PricingModel::FlatRate,
                    "membership" => PricingModel::Membership,
                    _ => panic!("Invalid pricing model in database"),
                };

                Pricing {
                    id: record.pricing_id,
                    network_id: NetworkId(record.network_id),
                    connector_type_id: record.connector_type_id.map(ConnectorTypeId),
                    pricing_model,
                    cost_per_kwh: record.cost_per_kwh,
                    cost_per_minute: record.cost_per_minute,
                    flat_rate_cost: record.flat_rate_cost,
                    membership_fee: record.membership_fee,
                    start_time: record.start_time,
                    end_time: record.end_time,
                    day_of_week: record.day_of_week,
                    is_active: record.is_active,
                    effective_from: record.effective_from,
                    effective_until: record.effective_until,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(pricing_rules)
    }

    pub async fn find_active_pricing_for_date_and_time(
        &self,
        network_id: NetworkId,
        connector_type_id: Option<ConnectorTypeId>,
        date: NaiveDate,
        time: NaiveTime,
    ) -> RepositoryResult<Vec<Pricing>> {
        let connector_type_id_value = connector_type_id.map(|id| id.0);
        let day_of_week = date.weekday().num_days_from_sunday() as i32;

        let records = sqlx::query!(
            r#"
            SELECT 
                pricing_id, network_id, connector_type_id,
                pricing_model as "pricing_model!: String",
                cost_per_kwh, cost_per_minute, flat_rate_cost, membership_fee,
                start_time, end_time, day_of_week,
                is_active, effective_from, effective_until,
                created_by, updated_by, created_at, updated_at
            FROM pricing
            WHERE network_id = $1
            AND (connector_type_id = $2 OR connector_type_id IS NULL)
            AND is_active = true
            AND effective_from <= $3
            AND (effective_until IS NULL OR effective_until >= $3)
            AND (day_of_week IS NULL OR day_of_week = $4)
            AND (
                (start_time IS NULL AND end_time IS NULL) OR -- No time restrictions
                (start_time <= $5 AND end_time >= $5) OR -- Within time window
                (start_time > end_time AND (start_time <= $5 OR end_time >= $5)) -- Overnight time window
            )
            ORDER BY 
                connector_type_id NULLS LAST, -- Prefer connector-specific pricing
                day_of_week NULLS LAST, -- Prefer day-specific pricing
                start_time NULLS LAST -- Prefer time-specific pricing
            "#,
            network_id.0,
            connector_type_id_value,
            date,
            day_of_week,
            time
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let pricing_rules = records
            .into_iter()
            .map(|record| {
                let pricing_model = match record.pricing_model.as_str() {
                    "per_kwh" => PricingModel::PerKWH,
                    "per_minute" => PricingModel::PerMinute,
                    "flat_rate" => PricingModel::FlatRate,
                    "membership" => PricingModel::Membership,
                    _ => panic!("Invalid pricing model in database"),
                };

                Pricing {
                    id: record.pricing_id,
                    network_id: NetworkId(record.network_id),
                    connector_type_id: record.connector_type_id.map(ConnectorTypeId),
                    pricing_model,
                    cost_per_kwh: record.cost_per_kwh,
                    cost_per_minute: record.cost_per_minute,
                    flat_rate_cost: record.flat_rate_cost,
                    membership_fee: record.membership_fee,
                    start_time: record.start_time,
                    end_time: record.end_time,
                    day_of_week: record.day_of_week,
                    is_active: record.is_active,
                    effective_from: record.effective_from,
                    effective_until: record.effective_until,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(pricing_rules)
    }

    pub async fn find_expired_pricing_rules(&self, current_date: NaiveDate) -> RepositoryResult<Vec<Pricing>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                pricing_id, network_id, connector_type_id,
                pricing_model as "pricing_model!: String",
                cost_per_kwh, cost_per_minute, flat_rate_cost, membership_fee,
                start_time, end_time, day_of_week,
                is_active, effective_from, effective_until,
                created_by, updated_by, created_at, updated_at
            FROM pricing
            WHERE effective_until IS NOT NULL 
            AND effective_until < $1
            AND is_active = true
            ORDER BY effective_until DESC
            "#,
            current_date
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let pricing_rules = records
            .into_iter()
            .map(|record| {
                let pricing_model = match record.pricing_model.as_str() {
                    "per_kwh" => PricingModel::PerKWH,
                    "per_minute" => PricingModel::PerMinute,
                    "flat_rate" => PricingModel::FlatRate,
                    "membership" => PricingModel::Membership,
                    _ => panic!("Invalid pricing model in database"),
                };

                Pricing {
                    id: record.pricing_id,
                    network_id: NetworkId(record.network_id),
                    connector_type_id: record.connector_type_id.map(ConnectorTypeId),
                    pricing_model,
                    cost_per_kwh: record.cost_per_kwh,
                    cost_per_minute: record.cost_per_minute,
                    flat_rate_cost: record.flat_rate_cost,
                    membership_fee: record.membership_fee,
                    start_time: record.start_time,
                    end_time: record.end_time,
                    day_of_week: record.day_of_week,
                    is_active: record.is_active,
                    effective_from: record.effective_from,
                    effective_until: record.effective_until,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(pricing_rules)
    }

    pub async fn deactivate_pricing_rule(&self, pricing_id: i32, updated_by: UserId) -> RepositoryResult<()> {
        let rows_affected = sqlx::query!(
            r#"
            UPDATE pricing 
            SET is_active = false, updated_by = $1, updated_at = CURRENT_TIMESTAMP
            WHERE pricing_id = $2
            "#,
            Uuid::from(updated_by.0),
            pricing_id
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

    pub async fn find_pricing_by_model(
        &self,
        pricing_model: PricingModel,
        is_active: Option<bool>,
    ) -> RepositoryResult<Vec<Pricing>> {
        let pricing_model_str = match pricing_model {
            PricingModel::PerKWH => "per_kwh",
            PricingModel::PerMinute => "per_minute",
            PricingModel::FlatRate => "flat_rate",
            PricingModel::Membership => "membership",
        };

        let query = match is_active {
            Some(active) => {
                sqlx::query!(
                    r#"
                    SELECT 
                        pricing_id, network_id, connector_type_id,
                        pricing_model as "pricing_model!: String",
                        cost_per_kwh, cost_per_minute, flat_rate_cost, membership_fee,
                        start_time, end_time, day_of_week,
                        is_active, effective_from, effective_until,
                        created_by, updated_by, created_at, updated_at
                    FROM pricing
                    WHERE pricing_model = $1 AND is_active = $2
                    ORDER BY effective_from DESC
                    "#,
                    pricing_model_str,
                    active
                )
            }
            None => {
                sqlx::query!(
                    r#"
                    SELECT 
                        pricing_id, network_id, connector_type_id,
                        pricing_model as "pricing_model!: String",
                        cost_per_kwh, cost_per_minute, flat_rate_cost, membership_fee,
                        start_time, end_time, day_of_week,
                        is_active, effective_from, effective_until,
                        created_by, updated_by, created_at, updated_at
                    FROM pricing
                    WHERE pricing_model = $1
                    ORDER BY effective_from DESC
                    "#,
                    pricing_model_str
                )
            }
        };

        let records = query
            .fetch_all(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let pricing_rules = records
            .into_iter()
            .map(|record| {
                let pricing_model = match record.pricing_model.as_str() {
                    "per_kwh" => PricingModel::PerKWH,
                    "per_minute" => PricingModel::PerMinute,
                    "flat_rate" => PricingModel::FlatRate,
                    "membership" => PricingModel::Membership,
                    _ => panic!("Invalid pricing model in database"),
                };

                Pricing {
                    id: record.pricing_id,
                    network_id: NetworkId(record.network_id),
                    connector_type_id: record.connector_type_id.map(ConnectorTypeId),
                    pricing_model,
                    cost_per_kwh: record.cost_per_kwh,
                    cost_per_minute: record.cost_per_minute,
                    flat_rate_cost: record.flat_rate_cost,
                    membership_fee: record.membership_fee,
                    start_time: record.start_time,
                    end_time: record.end_time,
                    day_of_week: record.day_of_week,
                    is_active: record.is_active,
                    effective_from: record.effective_from,
                    effective_until: record.effective_until,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(pricing_rules)
    }

    pub async fn get_pricing_history_for_network(
        &self,
        network_id: NetworkId,
        start_date: NaiveDate,
        end_date: NaiveDate,
    ) -> RepositoryResult<Vec<Pricing>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                pricing_id, network_id, connector_type_id,
                pricing_model as "pricing_model!: String",
                cost_per_kwh, cost_per_minute, flat_rate_cost, membership_fee,
                start_time, end_time, day_of_week,
                is_active, effective_from, effective_until,
                created_by, updated_by, created_at, updated_at
            FROM pricing
            WHERE network_id = $1
            AND (
                (effective_from BETWEEN $2 AND $3) OR
                (effective_until BETWEEN $2 AND $3) OR
                (effective_from <= $2 AND (effective_until IS NULL OR effective_until >= $3))
            )
            ORDER BY effective_from DESC, connector_type_id NULLS FIRST
            "#,
            network_id.0,
            start_date,
            end_date
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let pricing_rules = records
            .into_iter()
            .map(|record| {
                let pricing_model = match record.pricing_model.as_str() {
                    "per_kwh" => PricingModel::PerKWH,
                    "per_minute" => PricingModel::PerMinute,
                    "flat_rate" => PricingModel::FlatRate,
                    "membership" => PricingModel::Membership,
                    _ => panic!("Invalid pricing model in database"),
                };

                Pricing {
                    id: record.pricing_id,
                    network_id: NetworkId(record.network_id),
                    connector_type_id: record.connector_type_id.map(ConnectorTypeId),
                    pricing_model,
                    cost_per_kwh: record.cost_per_kwh,
                    cost_per_minute: record.cost_per_minute,
                    flat_rate_cost: record.flat_rate_cost,
                    membership_fee: record.membership_fee,
                    start_time: record.start_time,
                    end_time: record.end_time,
                    day_of_week: record.day_of_week,
                    is_active: record.is_active,
                    effective_from: record.effective_from,
                    effective_until: record.effective_until,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(pricing_rules)
    }
}