use crate::domain::entities::networks::Network;
use crate::domain::repositories::NetworkRepository;
use crate::shared::constants::NetworkType;
use crate::shared::errors::AppError;
use async_trait::async_trait;
use chrono::{DateTime, Utc};
use sqlx::PgPool;

#[derive(Debug, Clone)]
pub struct NetworkRepositoryImpl {
    pool: PgPool,
}

impl NetworkRepositoryImpl {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl NetworkRepository for NetworkRepositoryImpl {
    async fn find_by_id(&self, network_id: i32) -> Result<Option<Network>, AppError> {
        let record = sqlx::query!(
            r#"
            SELECT network_id, name, type, contact_email, phone_number, address,
                   created_by, updated_by, created_at, updated_at
            FROM networks 
            WHERE network_id = $1
            "#,
            network_id
        )
        .fetch_optional(&self.pool)
        .await?;

        let network = record.map(|r| {
            let network_type = match r.r#type.as_str() {
                "individual" => NetworkType::Individual,
                "company" => NetworkType::Company,
                _ => NetworkType::Individual,
            };

            Network {
                network_id: r.network_id,
                name: r.name,
                network_type,
                contact_email: r.contact_email,
                phone_number: r.phone_number,
                address: r.address,
                created_by: r.created_by,
                updated_by: r.updated_by,
                created_at: DateTime::from_naive_utc_and_offset(
                    r.created_at.unwrap_or_default(),
                    Utc,
                ), // Fixed
                updated_at: DateTime::from_naive_utc_and_offset(
                    r.updated_at.unwrap_or_default(),
                    Utc,
                ), // Fixed
            }
        });

        Ok(network)
    }

    async fn save(&self, network: &Network) -> Result<Network, AppError> {
        let saved_network = if network.network_id == 0 {
            // Insert new network
            let record = sqlx::query!(
                r#"
                INSERT INTO networks (name, type, contact_email, phone_number, address, created_by, updated_by)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING network_id, name, type, contact_email, phone_number, address,
                          created_by, updated_by, created_at, updated_at
                "#,
                network.name,
                network.network_type.as_str(),
                network.contact_email,
                network.phone_number,
                network.address,
                network.created_by,
                network.updated_by
            )
            .fetch_one(&self.pool)
            .await?;

            let network_type = match record.r#type.as_str() {
                "individual" => NetworkType::Individual,
                "company" => NetworkType::Company,
                _ => NetworkType::Individual,
            };

            Network {
                network_id: record.network_id,
                name: record.name,
                network_type,
                contact_email: record.contact_email,
                phone_number: record.phone_number,
                address: record.address,
                created_by: record.created_by,
                updated_by: record.updated_by,
                created_at: DateTime::from_naive_utc_and_offset(
                    record.created_at.unwrap_or_default(),
                    Utc,
                ), // Fixed
                updated_at: DateTime::from_naive_utc_and_offset(
                    record.updated_at.unwrap_or_default(),
                    Utc,
                ), // Fixed
            }
        } else {
            // Update existing network
            let record = sqlx::query!(
                r#"
                UPDATE networks 
                SET name = $1, type = $2, contact_email = $3, phone_number = $4, address = $5, 
                    updated_by = $6, updated_at = CURRENT_TIMESTAMP
                WHERE network_id = $7
                RETURNING network_id, name, type, contact_email, phone_number, address,
                          created_by, updated_by, created_at, updated_at
                "#,
                network.name,
                network.network_type.as_str(),
                network.contact_email,
                network.phone_number,
                network.address,
                network.updated_by,
                network.network_id
            )
            .fetch_one(&self.pool)
            .await?;

            let network_type = match record.r#type.as_str() {
                "individual" => NetworkType::Individual,
                "company" => NetworkType::Company,
                _ => NetworkType::Individual,
            };

            Network {
                network_id: record.network_id,
                name: record.name,
                network_type,
                contact_email: record.contact_email,
                phone_number: record.phone_number,
                address: record.address,
                created_by: record.created_by,
                updated_by: record.updated_by,
                created_at: DateTime::from_naive_utc_and_offset(
                    record.created_at.unwrap_or_default(),
                    Utc,
                ), // Fixed
                updated_at: DateTime::from_naive_utc_and_offset(
                    record.updated_at.unwrap_or_default(),
                    Utc,
                ), // Fixed
            }
        };

        Ok(saved_network)
    }

    async fn delete(&self, network_id: i32) -> Result<(), AppError> {
        let result = sqlx::query!("DELETE FROM networks WHERE network_id = $1", network_id)
            .execute(&self.pool)
            .await?;

        if result.rows_affected() == 0 {
            return Err(AppError::NotFound(format!(
                "Network with id {} not found",
                network_id
            )));
        }

        Ok(())
    }

    async fn find_all(&self, page: u32, page_size: u32) -> Result<Vec<Network>, AppError> {
        let offset = (page - 1) * page_size;

        let records = sqlx::query!(
            r#"
            SELECT network_id, name, type, contact_email, phone_number, address,
                   created_by, updated_by, created_at, updated_at
            FROM networks 
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
            "#,
            page_size as i64,
            offset as i64
        )
        .fetch_all(&self.pool)
        .await?;

        let networks = records
            .into_iter()
            .map(|r| {
                let network_type = match r.r#type.as_str() {
                    "individual" => NetworkType::Individual,
                    "company" => NetworkType::Company,
                    _ => NetworkType::Individual,
                };

                Network {
                    network_id: r.network_id,
                    name: r.name,
                    network_type,
                    contact_email: r.contact_email,
                    phone_number: r.phone_number,
                    address: r.address,
                    created_by: r.created_by,
                    updated_by: r.updated_by,
                    created_at: DateTime::from_naive_utc_and_offset(
                        r.created_at.unwrap_or_default(),
                        Utc,
                    ), // Fixed
                    updated_at: DateTime::from_naive_utc_and_offset(
                        r.updated_at.unwrap_or_default(),
                        Utc,
                    ), // Fixed
                }
            })
            .collect();

        Ok(networks)
    }
}
