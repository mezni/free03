use async_trait::async_trait;
use sqlx::{PgPool, Row};
use chrono::{DateTime, Utc};
use uuid::Uuid;

use crate::domain::models::Network;
use crate::domain::repositories::{NetworkRepository, RepositoryResult, RepositoryError};
use crate::domain::value_objects::{NetworkId, NetworkType, UserId};

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
    async fn find_by_id(&self, id: NetworkId) -> RepositoryResult<Option<Network>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                network_id, name, type as "type!: String", contact_email, phone_number, address,
                created_by, updated_by, created_at, updated_at
            FROM networks 
            WHERE network_id = $1
            "#,
            id.0
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let network_type = match record.type_.as_str() {
                    "individual" => NetworkType::Individual,
                    "company" => NetworkType::Company,
                    _ => return Err(RepositoryError::DatabaseError("Invalid network type".to_string())),
                };

                Ok(Some(Network {
                    id: NetworkId(record.network_id),
                    name: record.name,
                    network_type,
                    contact_email: record.contact_email,
                    phone_number: record.phone_number,
                    address: record.address,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn find_by_name(&self, name: &str) -> RepositoryResult<Option<Network>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                network_id, name, type as "type!: String", contact_email, phone_number, address,
                created_by, updated_by, created_at, updated_at
            FROM networks 
            WHERE name = $1
            "#,
            name
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let network_type = match record.type_.as_str() {
                    "individual" => NetworkType::Individual,
                    "company" => NetworkType::Company,
                    _ => return Err(RepositoryError::DatabaseError("Invalid network type".to_string())),
                };

                Ok(Some(Network {
                    id: NetworkId(record.network_id),
                    name: record.name,
                    network_type,
                    contact_email: record.contact_email,
                    phone_number: record.phone_number,
                    address: record.address,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn save(&self, network: &mut Network) -> RepositoryResult<()> {
        if network.id.0 == 0 {
            // Insert new network
            let result = sqlx::query!(
                r#"
                INSERT INTO networks (name, type, contact_email, phone_number, address, created_by, updated_by)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING network_id, created_at, updated_at
                "#,
                network.name,
                match network.network_type {
                    NetworkType::Individual => "individual",
                    NetworkType::Company => "company",
                },
                network.contact_email,
                network.phone_number,
                network.address,
                Uuid::from(network.created_by.0),
                network.updated_by.map(|user_id| Uuid::from(user_id.0))
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            network.id = NetworkId(result.network_id);
            network.created_at = result.created_at;
            network.updated_at = result.updated_at;
        } else {
            // Update existing network
            let result = sqlx::query!(
                r#"
                UPDATE networks 
                SET name = $1, type = $2, contact_email = $3, phone_number = $4, address = $5, 
                    updated_by = $6, updated_at = CURRENT_TIMESTAMP
                WHERE network_id = $7
                RETURNING updated_at
                "#,
                network.name,
                match network.network_type {
                    NetworkType::Individual => "individual",
                    NetworkType::Company => "company",
                },
                network.contact_email,
                network.phone_number,
                network.address,
                network.updated_by.map(|user_id| Uuid::from(user_id.0)),
                network.id.0
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            network.updated_at = result.updated_at;
        }

        Ok(())
    }

    async fn delete(&self, id: NetworkId) -> RepositoryResult<()> {
        let rows_affected = sqlx::query!(
            "DELETE FROM networks WHERE network_id = $1",
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

    async fn find_all(&self) -> RepositoryResult<Vec<Network>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                network_id, name, type as "type!: String", contact_email, phone_number, address,
                created_by, updated_by, created_at, updated_at
            FROM networks
            ORDER BY name
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let networks = records
            .into_iter()
            .map(|record| {
                let network_type = match record.type_.as_str() {
                    "individual" => NetworkType::Individual,
                    "company" => NetworkType::Company,
                    _ => panic!("Invalid network type in database"),
                };

                Network {
                    id: NetworkId(record.network_id),
                    name: record.name,
                    network_type,
                    contact_email: record.contact_email,
                    phone_number: record.phone_number,
                    address: record.address,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(networks)
    }

    async fn find_by_type(&self, network_type: NetworkType) -> RepositoryResult<Vec<Network>> {
        let type_str = match network_type {
            NetworkType::Individual => "individual",
            NetworkType::Company => "company",
        };

        let records = sqlx::query!(
            r#"
            SELECT 
                network_id, name, type as "type!: String", contact_email, phone_number, address,
                created_by, updated_by, created_at, updated_at
            FROM networks
            WHERE type = $1
            ORDER BY name
            "#,
            type_str
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let networks = records
            .into_iter()
            .map(|record| {
                let network_type = match record.type_.as_str() {
                    "individual" => NetworkType::Individual,
                    "company" => NetworkType::Company,
                    _ => panic!("Invalid network type in database"),
                };

                Network {
                    id: NetworkId(record.network_id),
                    name: record.name,
                    network_type,
                    contact_email: record.contact_email,
                    phone_number: record.phone_number,
                    address: record.address,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(networks)
    }
}