use async_trait::async_trait;
use sqlx::PgPool;
use uuid::Uuid;
use chrono::{DateTime, Utc};

use crate::domain::models::ChargingSession;
use crate::domain::repositories::{ChargingSessionRepository, RepositoryResult, RepositoryError};
use crate::domain::value_objects::{
    ChargingSessionId, ConnectorId, UserId, EnergyKWH, Money, 
    ChargingSessionStatus, PaymentStatus
};

pub struct ChargingSessionRepositoryImpl {
    pool: PgPool,
}

impl ChargingSessionRepositoryImpl {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl ChargingSessionRepository for ChargingSessionRepositoryImpl {
    async fn find_by_id(&self, id: ChargingSessionId) -> RepositoryResult<Option<ChargingSession>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                session_id, connector_id, user_id, start_time, end_time,
                energy_delivered_kwh, total_cost, 
                payment_status as "payment_status!: String",
                payment_method,
                session_status as "session_status!: String",
                initiated_by, ended_by, created_at, updated_at
            FROM charging_sessions 
            WHERE session_id = $1
            "#,
            id.0
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let session_status = match record.session_status.as_str() {
                    "active" => ChargingSessionStatus::Active,
                    "completed" => ChargingSessionStatus::Completed,
                    "cancelled" => ChargingSessionStatus::Cancelled,
                    "interrupted" => ChargingSessionStatus::Interrupted,
                    _ => return Err(RepositoryError::DatabaseError("Invalid session status".to_string())),
                };

                let payment_status = match record.payment_status.as_str() {
                    "pending" => PaymentStatus::Pending,
                    "paid" => PaymentStatus::Paid,
                    "failed" => PaymentStatus::Failed,
                    "refunded" => PaymentStatus::Refunded,
                    _ => return Err(RepositoryError::DatabaseError("Invalid payment status".to_string())),
                };

                let energy_delivered_kwh = record.energy_delivered_kwh
                    .map(|energy| EnergyKWH::new(energy)
                        .map_err(|e| RepositoryError::DatabaseError(e.to_string())))
                    .transpose()?;

                let total_cost = record.total_cost
                    .map(|cost| Money::new(cost, "USD") // Assuming USD for now
                        .map_err(|e| RepositoryError::DatabaseError(e.to_string())))
                    .transpose()?;

                Ok(Some(ChargingSession {
                    id: ChargingSessionId(record.session_id),
                    connector_id: ConnectorId(record.connector_id),
                    user_id: UserId::parse_str(&record.user_id.to_string()).unwrap(),
                    start_time: record.start_time,
                    end_time: record.end_time,
                    energy_delivered_kwh,
                    total_cost,
                    payment_status,
                    payment_method: record.payment_method,
                    session_status,
                    initiated_by: UserId::parse_str(&record.initiated_by.to_string()).unwrap(),
                    ended_by: record.ended_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn find_by_user_id(&self, user_id: UserId) -> RepositoryResult<Vec<ChargingSession>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                session_id, connector_id, user_id, start_time, end_time,
                energy_delivered_kwh, total_cost, 
                payment_status as "payment_status!: String",
                payment_method,
                session_status as "session_status!: String",
                initiated_by, ended_by, created_at, updated_at
            FROM charging_sessions
            WHERE user_id = $1
            ORDER BY start_time DESC
            "#,
            Uuid::from(user_id.0)
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let sessions = records
            .into_iter()
            .map(|record| {
                let session_status = match record.session_status.as_str() {
                    "active" => ChargingSessionStatus::Active,
                    "completed" => ChargingSessionStatus::Completed,
                    "cancelled" => ChargingSessionStatus::Cancelled,
                    "interrupted" => ChargingSessionStatus::Interrupted,
                    _ => panic!("Invalid session status in database"),
                };

                let payment_status = match record.payment_status.as_str() {
                    "pending" => PaymentStatus::Pending,
                    "paid" => PaymentStatus::Paid,
                    "failed" => PaymentStatus::Failed,
                    "refunded" => PaymentStatus::Refunded,
                    _ => panic!("Invalid payment status in database"),
                };

                let energy_delivered_kwh = record.energy_delivered_kwh
                    .map(|energy| EnergyKWH::new(energy).expect("Invalid energy value in database"));

                let total_cost = record.total_cost
                    .map(|cost| Money::new(cost, "USD").expect("Invalid cost value in database"));

                ChargingSession {
                    id: ChargingSessionId(record.session_id),
                    connector_id: ConnectorId(record.connector_id),
                    user_id: UserId::parse_str(&record.user_id.to_string()).unwrap(),
                    start_time: record.start_time,
                    end_time: record.end_time,
                    energy_delivered_kwh,
                    total_cost,
                    payment_status,
                    payment_method: record.payment_method,
                    session_status,
                    initiated_by: UserId::parse_str(&record.initiated_by.to_string()).unwrap(),
                    ended_by: record.ended_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(sessions)
    }

    async fn find_by_connector_id(&self, connector_id: ConnectorId) -> RepositoryResult<Vec<ChargingSession>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                session_id, connector_id, user_id, start_time, end_time,
                energy_delivered_kwh, total_cost, 
                payment_status as "payment_status!: String",
                payment_method,
                session_status as "session_status!: String",
                initiated_by, ended_by, created_at, updated_at
            FROM charging_sessions
            WHERE connector_id = $1
            ORDER BY start_time DESC
            "#,
            connector_id.0
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let sessions = records
            .into_iter()
            .map(|record| {
                let session_status = match record.session_status.as_str() {
                    "active" => ChargingSessionStatus::Active,
                    "completed" => ChargingSessionStatus::Completed,
                    "cancelled" => ChargingSessionStatus::Cancelled,
                    "interrupted" => ChargingSessionStatus::Interrupted,
                    _ => panic!("Invalid session status in database"),
                };

                let payment_status = match record.payment_status.as_str() {
                    "pending" => PaymentStatus::Pending,
                    "paid" => PaymentStatus::Paid,
                    "failed" => PaymentStatus::Failed,
                    "refunded" => PaymentStatus::Refunded,
                    _ => panic!("Invalid payment status in database"),
                };

                let energy_delivered_kwh = record.energy_delivered_kwh
                    .map(|energy| EnergyKWH::new(energy).expect("Invalid energy value in database"));

                let total_cost = record.total_cost
                    .map(|cost| Money::new(cost, "USD").expect("Invalid cost value in database"));

                ChargingSession {
                    id: ChargingSessionId(record.session_id),
                    connector_id: ConnectorId(record.connector_id),
                    user_id: UserId::parse_str(&record.user_id.to_string()).unwrap(),
                    start_time: record.start_time,
                    end_time: record.end_time,
                    energy_delivered_kwh,
                    total_cost,
                    payment_status,
                    payment_method: record.payment_method,
                    session_status,
                    initiated_by: UserId::parse_str(&record.initiated_by.to_string()).unwrap(),
                    ended_by: record.ended_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(sessions)
    }

    async fn find_active_sessions(&self) -> RepositoryResult<Vec<ChargingSession>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                session_id, connector_id, user_id, start_time, end_time,
                energy_delivered_kwh, total_cost, 
                payment_status as "payment_status!: String",
                payment_method,
                session_status as "session_status!: String",
                initiated_by, ended_by, created_at, updated_at
            FROM charging_sessions
            WHERE session_status = 'active'
            ORDER BY start_time
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let sessions = records
            .into_iter()
            .map(|record| {
                let session_status = match record.session_status.as_str() {
                    "active" => ChargingSessionStatus::Active,
                    _ => panic!("Expected active status in database"),
                };

                let payment_status = match record.payment_status.as_str() {
                    "pending" => PaymentStatus::Pending,
                    "paid" => PaymentStatus::Paid,
                    "failed" => PaymentStatus::Failed,
                    "refunded" => PaymentStatus::Refunded,
                    _ => panic!("Invalid payment status in database"),
                };

                let energy_delivered_kwh = record.energy_delivered_kwh
                    .map(|energy| EnergyKWH::new(energy).expect("Invalid energy value in database"));

                let total_cost = record.total_cost
                    .map(|cost| Money::new(cost, "USD").expect("Invalid cost value in database"));

                ChargingSession {
                    id: ChargingSessionId(record.session_id),
                    connector_id: ConnectorId(record.connector_id),
                    user_id: UserId::parse_str(&record.user_id.to_string()).unwrap(),
                    start_time: record.start_time,
                    end_time: record.end_time,
                    energy_delivered_kwh,
                    total_cost,
                    payment_status,
                    payment_method: record.payment_method,
                    session_status,
                    initiated_by: UserId::parse_str(&record.initiated_by.to_string()).unwrap(),
                    ended_by: record.ended_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(sessions)
    }

    async fn find_sessions_in_date_range(
        &self,
        start_date: DateTime<Utc>,
        end_date: DateTime<Utc>,
    ) -> RepositoryResult<Vec<ChargingSession>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                session_id, connector_id, user_id, start_time, end_time,
                energy_delivered_kwh, total_cost, 
                payment_status as "payment_status!: String",
                payment_method,
                session_status as "session_status!: String",
                initiated_by, ended_by, created_at, updated_at
            FROM charging_sessions
            WHERE start_time BETWEEN $1 AND $2
            ORDER BY start_time
            "#,
            start_date,
            end_date
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let sessions = records
            .into_iter()
            .map(|record| {
                let session_status = match record.session_status.as_str() {
                    "active" => ChargingSessionStatus::Active,
                    "completed" => ChargingSessionStatus::Completed,
                    "cancelled" => ChargingSessionStatus::Cancelled,
                    "interrupted" => ChargingSessionStatus::Interrupted,
                    _ => panic!("Invalid session status in database"),
                };

                let payment_status = match record.payment_status.as_str() {
                    "pending" => PaymentStatus::Pending,
                    "paid" => PaymentStatus::Paid,
                    "failed" => PaymentStatus::Failed,
                    "refunded" => PaymentStatus::Refunded,
                    _ => panic!("Invalid payment status in database"),
                };

                let energy_delivered_kwh = record.energy_delivered_kwh
                    .map(|energy| EnergyKWH::new(energy).expect("Invalid energy value in database"));

                let total_cost = record.total_cost
                    .map(|cost| Money::new(cost, "USD").expect("Invalid cost value in database"));

                ChargingSession {
                    id: ChargingSessionId(record.session_id),
                    connector_id: ConnectorId(record.connector_id),
                    user_id: UserId::parse_str(&record.user_id.to_string()).unwrap(),
                    start_time: record.start_time,
                    end_time: record.end_time,
                    energy_delivered_kwh,
                    total_cost,
                    payment_status,
                    payment_method: record.payment_method,
                    session_status,
                    initiated_by: UserId::parse_str(&record.initiated_by.to_string()).unwrap(),
                    ended_by: record.ended_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(sessions)
    }

    async fn save(&self, session: &mut ChargingSession) -> RepositoryResult<()> {
        let session_status_str = match session.session_status {
            ChargingSessionStatus::Active => "active",
            ChargingSessionStatus::Completed => "completed",
            ChargingSessionStatus::Cancelled => "cancelled",
            ChargingSessionStatus::Interrupted => "interrupted",
        };

        let payment_status_str = match session.payment_status {
            PaymentStatus::Pending => "pending",
            PaymentStatus::Paid => "paid",
            PaymentStatus::Failed => "failed",
            PaymentStatus::Refunded => "refunded",
        };

        if session.id.0 == 0 {
            // Insert new session
            let result = sqlx::query!(
                r#"
                INSERT INTO charging_sessions (
                    connector_id, user_id, start_time, end_time, energy_delivered_kwh,
                    total_cost, payment_status, payment_method, session_status,
                    initiated_by, ended_by
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
                RETURNING session_id, created_at, updated_at
                "#,
                session.connector_id.0,
                Uuid::from(session.user_id.0),
                session.start_time,
                session.end_time,
                session.energy_delivered_kwh.map(|e| e.0),
                session.total_cost.map(|c| c.amount),
                payment_status_str,
                session.payment_method,
                session_status_str,
                Uuid::from(session.initiated_by.0),
                session.ended_by.map(|user_id| Uuid::from(user_id.0))
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            session.id = ChargingSessionId(result.session_id);
            session.created_at = result.created_at;
            session.updated_at = result.updated_at;
        } else {
            // Update existing session
            let result = sqlx::query!(
                r#"
                UPDATE charging_sessions 
                SET connector_id = $1, user_id = $2, start_time = $3, end_time = $4,
                    energy_delivered_kwh = $5, total_cost = $6, payment_status = $7,
                    payment_method = $8, session_status = $9, initiated_by = $10,
                    ended_by = $11, updated_at = CURRENT_TIMESTAMP
                WHERE session_id = $12
                RETURNING updated_at
                "#,
                session.connector_id.0,
                Uuid::from(session.user_id.0),
                session.start_time,
                session.end_time,
                session.energy_delivered_kwh.map(|e| e.0),
                session.total_cost.map(|c| c.amount),
                payment_status_str,
                session.payment_method,
                session_status_str,
                Uuid::from(session.initiated_by.0),
                session.ended_by.map(|user_id| Uuid::from(user_id.0)),
                session.id.0
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            session.updated_at = result.updated_at;
        }

        Ok(())
    }

    async fn delete(&self, id: ChargingSessionId) -> RepositoryResult<()> {
        let rows_affected = sqlx::query!(
            "DELETE FROM charging_sessions WHERE session_id = $1",
            id.0
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

// Additional utility methods for charging sessions
impl ChargingSessionRepositoryImpl {
    pub async fn find_active_session_by_connector(
        &self, 
        connector_id: ConnectorId
    ) -> RepositoryResult<Option<ChargingSession>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                session_id, connector_id, user_id, start_time, end_time,
                energy_delivered_kwh, total_cost, 
                payment_status as "payment_status!: String",
                payment_method,
                session_status as "session_status!: String",
                initiated_by, ended_by, created_at, updated_at
            FROM charging_sessions 
            WHERE connector_id = $1 AND session_status = 'active'
            "#,
            connector_id.0
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let session_status = match record.session_status.as_str() {
                    "active" => ChargingSessionStatus::Active,
                    _ => return Err(RepositoryError::DatabaseError("Expected active session status".to_string())),
                };

                let payment_status = match record.payment_status.as_str() {
                    "pending" => PaymentStatus::Pending,
                    "paid" => PaymentStatus::Paid,
                    "failed" => PaymentStatus::Failed,
                    "refunded" => PaymentStatus::Refunded,
                    _ => return Err(RepositoryError::DatabaseError("Invalid payment status".to_string())),
                };

                let energy_delivered_kwh = record.energy_delivered_kwh
                    .map(|energy| EnergyKWH::new(energy)
                        .map_err(|e| RepositoryError::DatabaseError(e.to_string())))
                    .transpose()?;

                let total_cost = record.total_cost
                    .map(|cost| Money::new(cost, "USD")
                        .map_err(|e| RepositoryError::DatabaseError(e.to_string())))
                    .transpose()?;

                Ok(Some(ChargingSession {
                    id: ChargingSessionId(record.session_id),
                    connector_id: ConnectorId(record.connector_id),
                    user_id: UserId::parse_str(&record.user_id.to_string()).unwrap(),
                    start_time: record.start_time,
                    end_time: record.end_time,
                    energy_delivered_kwh,
                    total_cost,
                    payment_status,
                    payment_method: record.payment_method,
                    session_status,
                    initiated_by: UserId::parse_str(&record.initiated_by.to_string()).unwrap(),
                    ended_by: record.ended_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    pub async fn find_recent_sessions_by_user(
        &self, 
        user_id: UserId, 
        limit: i64
    ) -> RepositoryResult<Vec<ChargingSession>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                session_id, connector_id, user_id, start_time, end_time,
                energy_delivered_kwh, total_cost, 
                payment_status as "payment_status!: String",
                payment_method,
                session_status as "session_status!: String",
                initiated_by, ended_by, created_at, updated_at
            FROM charging_sessions
            WHERE user_id = $1
            ORDER BY start_time DESC
            LIMIT $2
            "#,
            Uuid::from(user_id.0),
            limit
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let sessions = records
            .into_iter()
            .map(|record| {
                let session_status = match record.session_status.as_str() {
                    "active" => ChargingSessionStatus::Active,
                    "completed" => ChargingSessionStatus::Completed,
                    "cancelled" => ChargingSessionStatus::Cancelled,
                    "interrupted" => ChargingSessionStatus::Interrupted,
                    _ => panic!("Invalid session status in database"),
                };

                let payment_status = match record.payment_status.as_str() {
                    "pending" => PaymentStatus::Pending,
                    "paid" => PaymentStatus::Paid,
                    "failed" => PaymentStatus::Failed,
                    "refunded" => PaymentStatus::Refunded,
                    _ => panic!("Invalid payment status in database"),
                };

                let energy_delivered_kwh = record.energy_delivered_kwh
                    .map(|energy| EnergyKWH::new(energy).expect("Invalid energy value in database"));

                let total_cost = record.total_cost
                    .map(|cost| Money::new(cost, "USD").expect("Invalid cost value in database"));

                ChargingSession {
                    id: ChargingSessionId(record.session_id),
                    connector_id: ConnectorId(record.connector_id),
                    user_id: UserId::parse_str(&record.user_id.to_string()).unwrap(),
                    start_time: record.start_time,
                    end_time: record.end_time,
                    energy_delivered_kwh,
                    total_cost,
                    payment_status,
                    payment_method: record.payment_method,
                    session_status,
                    initiated_by: UserId::parse_str(&record.initiated_by.to_string()).unwrap(),
                    ended_by: record.ended_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(sessions)
    }

    pub async fn get_session_statistics(
        &self,
        start_date: DateTime<Utc>,
        end_date: DateTime<Utc>,
    ) -> RepositoryResult<SessionStatistics> {
        let stats = sqlx::query!(
            r#"
            SELECT 
                COUNT(*) as total_sessions,
                COUNT(*) FILTER (WHERE session_status = 'completed') as completed_sessions,
                COUNT(*) FILTER (WHERE session_status = 'active') as active_sessions,
                COUNT(*) FILTER (WHERE session_status = 'cancelled') as cancelled_sessions,
                COALESCE(SUM(energy_delivered_kwh), 0) as total_energy_kwh,
                COALESCE(SUM(total_cost), 0) as total_revenue
            FROM charging_sessions
            WHERE start_time BETWEEN $1 AND $2
            "#,
            start_date,
            end_date
        )
        .fetch_one(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        Ok(SessionStatistics {
            total_sessions: stats.total_sessions.unwrap_or(0) as u64,
            completed_sessions: stats.completed_sessions.unwrap_or(0) as u64,
            active_sessions: stats.active_sessions.unwrap_or(0) as u64,
            cancelled_sessions: stats.cancelled_sessions.unwrap_or(0) as u64,
            total_energy_kwh: stats.total_energy_kwh.unwrap_or(0.0),
            total_revenue: stats.total_revenue.unwrap_or(0.0),
        })
    }
}

#[derive(Debug, Clone)]
pub struct SessionStatistics {
    pub total_sessions: u64,
    pub completed_sessions: u64,
    pub active_sessions: u64,
    pub cancelled_sessions: u64,
    pub total_energy_kwh: f64,
    pub total_revenue: f64,
}