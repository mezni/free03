use async_trait::async_trait;
use sqlx::PgPool;
use uuid::Uuid;

use crate::domain::models::ConnectorType;
use crate::domain::repositories::{ConnectorTypeRepository, RepositoryResult, RepositoryError};
use crate::domain::value_objects::{ConnectorTypeId, CurrentType, PowerKW, UserId};

pub struct ConnectorTypeRepositoryImpl {
    pool: PgPool,
}

impl ConnectorTypeRepositoryImpl {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl ConnectorTypeRepository for ConnectorTypeRepositoryImpl {
    async fn find_by_id(&self, id: ConnectorTypeId) -> RepositoryResult<Option<ConnectorType>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                connector_type_id, name, description, standard,
                current_type as "current_type!: String", typical_power_kw,
                pin_configuration, is_public_standard,
                created_by, updated_by, created_at, updated_at
            FROM connector_types 
            WHERE connector_type_id = $1
            "#,
            id.0
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let current_type = match record.current_type.as_str() {
                    "AC" => CurrentType::AC,
                    "DC" => CurrentType::DC,
                    _ => return Err(RepositoryError::DatabaseError("Invalid current type".to_string())),
                };

                let typical_power_kw = record.typical_power_kw
                    .map(|power| PowerKW::new(power)
                        .map_err(|e| RepositoryError::DatabaseError(e.to_string())))
                    .transpose()?;

                Ok(Some(ConnectorType {
                    id: ConnectorTypeId(record.connector_type_id),
                    name: record.name,
                    description: record.description,
                    standard: record.standard,
                    current_type,
                    typical_power_kw,
                    pin_configuration: record.pin_configuration,
                    is_public_standard: record.is_public_standard,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn find_by_name(&self, name: &str) -> RepositoryResult<Option<ConnectorType>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                connector_type_id, name, description, standard,
                current_type as "current_type!: String", typical_power_kw,
                pin_configuration, is_public_standard,
                created_by, updated_by, created_at, updated_at
            FROM connector_types 
            WHERE name = $1
            "#,
            name
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let current_type = match record.current_type.as_str() {
                    "AC" => CurrentType::AC,
                    "DC" => CurrentType::DC,
                    _ => return Err(RepositoryError::DatabaseError("Invalid current type".to_string())),
                };

                let typical_power_kw = record.typical_power_kw
                    .map(|power| PowerKW::new(power)
                        .map_err(|e| RepositoryError::DatabaseError(e.to_string())))
                    .transpose()?;

                Ok(Some(ConnectorType {
                    id: ConnectorTypeId(record.connector_type_id),
                    name: record.name,
                    description: record.description,
                    standard: record.standard,
                    current_type,
                    typical_power_kw,
                    pin_configuration: record.pin_configuration,
                    is_public_standard: record.is_public_standard,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn find_by_current_type(&self, current_type: CurrentType) -> RepositoryResult<Vec<ConnectorType>> {
        let current_type_str = match current_type {
            CurrentType::AC => "AC",
            CurrentType::DC => "DC",
        };

        let records = sqlx::query!(
            r#"
            SELECT 
                connector_type_id, name, description, standard,
                current_type as "current_type!: String", typical_power_kw,
                pin_configuration, is_public_standard,
                created_by, updated_by, created_at, updated_at
            FROM connector_types
            WHERE current_type = $1
            ORDER BY name
            "#,
            current_type_str
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let connector_types = records
            .into_iter()
            .map(|record| {
                let current_type = match record.current_type.as_str() {
                    "AC" => CurrentType::AC,
                    "DC" => CurrentType::DC,
                    _ => panic!("Invalid current type in database"),
                };

                let typical_power_kw = record.typical_power_kw
                    .map(|power| PowerKW::new(power).expect("Invalid power value in database"));

                ConnectorType {
                    id: ConnectorTypeId(record.connector_type_id),
                    name: record.name,
                    description: record.description,
                    standard: record.standard,
                    current_type,
                    typical_power_kw,
                    pin_configuration: record.pin_configuration,
                    is_public_standard: record.is_public_standard,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(connector_types)
    }

    async fn save(&self, connector_type: &mut ConnectorType) -> RepositoryResult<()> {
        let current_type_str = match connector_type.current_type {
            CurrentType::AC => "AC",
            CurrentType::DC => "DC",
        };

        if connector_type.id.0 == 0 {
            // Insert new connector type
            let result = sqlx::query!(
                r#"
                INSERT INTO connector_types (
                    name, description, standard, current_type, typical_power_kw,
                    pin_configuration, is_public_standard, created_by, updated_by
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                RETURNING connector_type_id, created_at, updated_at
                "#,
                connector_type.name,
                connector_type.description,
                connector_type.standard,
                current_type_str,
                connector_type.typical_power_kw.map(|p| p.0),
                connector_type.pin_configuration,
                connector_type.is_public_standard,
                Uuid::from(connector_type.created_by.0),
                connector_type.updated_by.map(|user_id| Uuid::from(user_id.0))
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            connector_type.id = ConnectorTypeId(result.connector_type_id);
            connector_type.created_at = result.created_at;
            connector_type.updated_at = result.updated_at;
        } else {
            // Update existing connector type
            let result = sqlx::query!(
                r#"
                UPDATE connector_types 
                SET name = $1, description = $2, standard = $3, current_type = $4,
                    typical_power_kw = $5, pin_configuration = $6, is_public_standard = $7,
                    updated_by = $8, updated_at = CURRENT_TIMESTAMP
                WHERE connector_type_id = $9
                RETURNING updated_at
                "#,
                connector_type.name,
                connector_type.description,
                connector_type.standard,
                current_type_str,
                connector_type.typical_power_kw.map(|p| p.0),
                connector_type.pin_configuration,
                connector_type.is_public_standard,
                connector_type.updated_by.map(|user_id| Uuid::from(user_id.0)),
                connector_type.id.0
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            connector_type.updated_at = result.updated_at;
        }

        Ok(())
    }

    async fn delete(&self, id: ConnectorTypeId) -> RepositoryResult<()> {
        // First check if there are any connectors using this type
        let connectors_count = sqlx::query!(
            "SELECT COUNT(*) as count FROM connectors WHERE connector_type_id = $1",
            id.0
        )
        .fetch_one(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?
        .count
        .unwrap_or(0);

        if connectors_count > 0 {
            return Err(RepositoryError::ConstraintViolation(
                format!("Cannot delete connector type with ID {} because it is used by {} connectors", id.0, connectors_count)
            ));
        }

        let rows_affected = sqlx::query!(
            "DELETE FROM connector_types WHERE connector_type_id = $1",
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

    async fn find_all(&self) -> RepositoryResult<Vec<ConnectorType>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                connector_type_id, name, description, standard,
                current_type as "current_type!: String", typical_power_kw,
                pin_configuration, is_public_standard,
                created_by, updated_by, created_at, updated_at
            FROM connector_types
            ORDER BY name
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let connector_types = records
            .into_iter()
            .map(|record| {
                let current_type = match record.current_type.as_str() {
                    "AC" => CurrentType::AC,
                    "DC" => CurrentType::DC,
                    _ => panic!("Invalid current type in database"),
                };

                let typical_power_kw = record.typical_power_kw
                    .map(|power| PowerKW::new(power).expect("Invalid power value in database"));

                ConnectorType {
                    id: ConnectorTypeId(record.connector_type_id),
                    name: record.name,
                    description: record.description,
                    standard: record.standard,
                    current_type,
                    typical_power_kw,
                    pin_configuration: record.pin_configuration,
                    is_public_standard: record.is_public_standard,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(connector_types)
    }
}

// Additional utility methods for connector type repository
impl ConnectorTypeRepositoryImpl {
    pub async fn find_by_standard(&self, standard: &str) -> RepositoryResult<Vec<ConnectorType>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                connector_type_id, name, description, standard,
                current_type as "current_type!: String", typical_power_kw,
                pin_configuration, is_public_standard,
                created_by, updated_by, created_at, updated_at
            FROM connector_types
            WHERE standard = $1
            ORDER BY name
            "#,
            standard
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let connector_types = records
            .into_iter()
            .map(|record| {
                let current_type = match record.current_type.as_str() {
                    "AC" => CurrentType::AC,
                    "DC" => CurrentType::DC,
                    _ => panic!("Invalid current type in database"),
                };

                let typical_power_kw = record.typical_power_kw
                    .map(|power| PowerKW::new(power).expect("Invalid power value in database"));

                ConnectorType {
                    id: ConnectorTypeId(record.connector_type_id),
                    name: record.name,
                    description: record.description,
                    standard: record.standard,
                    current_type,
                    typical_power_kw,
                    pin_configuration: record.pin_configuration,
                    is_public_standard: record.is_public_standard,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(connector_types)
    }

    pub async fn find_public_standards(&self) -> RepositoryResult<Vec<ConnectorType>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                connector_type_id, name, description, standard,
                current_type as "current_type!: String", typical_power_kw,
                pin_configuration, is_public_standard,
                created_by, updated_by, created_at, updated_at
            FROM connector_types
            WHERE is_public_standard = true
            ORDER BY name
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let connector_types = records
            .into_iter()
            .map(|record| {
                let current_type = match record.current_type.as_str() {
                    "AC" => CurrentType::AC,
                    "DC" => CurrentType::DC,
                    _ => panic!("Invalid current type in database"),
                };

                let typical_power_kw = record.typical_power_kw
                    .map(|power| PowerKW::new(power).expect("Invalid power value in database"));

                ConnectorType {
                    id: ConnectorTypeId(record.connector_type_id),
                    name: record.name,
                    description: record.description,
                    standard: record.standard,
                    current_type,
                    typical_power_kw,
                    pin_configuration: record.pin_configuration,
                    is_public_standard: record.is_public_standard,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(connector_types)
    }

    pub async fn find_proprietary_standards(&self) -> RepositoryResult<Vec<ConnectorType>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                connector_type_id, name, description, standard,
                current_type as "current_type!: String", typical_power_kw,
                pin_configuration, is_public_standard,
                created_by, updated_by, created_at, updated_at
            FROM connector_types
            WHERE is_public_standard = false
            ORDER BY name
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let connector_types = records
            .into_iter()
            .map(|record| {
                let current_type = match record.current_type.as_str() {
                    "AC" => CurrentType::AC,
                    "DC" => CurrentType::DC,
                    _ => panic!("Invalid current type in database"),
                };

                let typical_power_kw = record.typical_power_kw
                    .map(|power| PowerKW::new(power).expect("Invalid power value in database"));

                ConnectorType {
                    id: ConnectorTypeId(record.connector_type_id),
                    name: record.name,
                    description: record.description,
                    standard: record.standard,
                    current_type,
                    typical_power_kw,
                    pin_configuration: record.pin_configuration,
                    is_public_standard: record.is_public_standard,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(connector_types)
    }

    pub async fn find_high_power_connectors(&self, min_power_kw: f64) -> RepositoryResult<Vec<ConnectorType>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                connector_type_id, name, description, standard,
                current_type as "current_type!: String", typical_power_kw,
                pin_configuration, is_public_standard,
                created_by, updated_by, created_at, updated_at
            FROM connector_types
            WHERE typical_power_kw >= $1
            ORDER BY typical_power_kw DESC
            "#,
            min_power_kw
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let connector_types = records
            .into_iter()
            .map(|record| {
                let current_type = match record.current_type.as_str() {
                    "AC" => CurrentType::AC,
                    "DC" => CurrentType::DC,
                    _ => panic!("Invalid current type in database"),
                };

                let typical_power_kw = record.typical_power_kw
                    .map(|power| PowerKW::new(power).expect("Invalid power value in database"));

                ConnectorType {
                    id: ConnectorTypeId(record.connector_type_id),
                    name: record.name,
                    description: record.description,
                    standard: record.standard,
                    current_type,
                    typical_power_kw,
                    pin_configuration: record.pin_configuration,
                    is_public_standard: record.is_public_standard,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(connector_types)
    }

    pub async fn connector_type_exists_by_name(&self, name: &str) -> RepositoryResult<bool> {
        let result = sqlx::query!(
            "SELECT 1 FROM connector_types WHERE name = $1",
            name
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        Ok(result.is_some())
    }

    pub async fn get_connector_type_usage_stats(&self) -> RepositoryResult<Vec<ConnectorTypeUsage>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                ct.connector_type_id,
                ct.name,
                ct.current_type,
                COUNT(c.connector_id) as connector_count,
                COUNT(DISTINCT c.station_id) as station_count,
                COUNT(DISTINCT s.network_id) as network_count
            FROM connector_types ct
            LEFT JOIN connectors c ON ct.connector_type_id = c.connector_type_id
            LEFT JOIN stations s ON c.station_id = s.station_id
            GROUP BY ct.connector_type_id, ct.name, ct.current_type
            ORDER BY connector_count DESC
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let usage_stats = records
            .into_iter()
            .map(|record| {
                let current_type = match record.current_type.as_str() {
                    "AC" => CurrentType::AC,
                    "DC" => CurrentType::DC,
                    _ => panic!("Invalid current type in database"),
                };

                ConnectorTypeUsage {
                    connector_type_id: ConnectorTypeId(record.connector_type_id),
                    name: record.name,
                    current_type,
                    connector_count: record.connector_count.unwrap_or(0) as u64,
                    station_count: record.station_count.unwrap_or(0) as u64,
                    network_count: record.network_count.unwrap_or(0) as u64,
                }
            })
            .collect();

        Ok(usage_stats)
    }
}

#[derive(Debug, Clone)]
pub struct ConnectorTypeUsage {
    pub connector_type_id: ConnectorTypeId,
    pub name: String,
    pub current_type: CurrentType,
    pub connector_count: u64,
    pub station_count: u64,
    pub network_count: u64,
}