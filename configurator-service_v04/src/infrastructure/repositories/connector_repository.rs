use async_trait::async_trait;
use sqlx::PgPool;
use uuid::Uuid;

use crate::domain::models::Connector;
use crate::domain::repositories::{ConnectorRepository, RepositoryResult, RepositoryError};
use crate::domain::value_objects::{ConnectorId, StationId, ConnectorTypeId, PowerKW, ConnectorStatus, UserId};

pub struct ConnectorRepositoryImpl {
    pool: PgPool,
}

impl ConnectorRepositoryImpl {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl ConnectorRepository for ConnectorRepositoryImpl {
    async fn find_by_id(&self, id: ConnectorId) -> RepositoryResult<Option<Connector>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                connector_id, station_id, connector_type_id, power_level_kw, 
                status as "status!: String", max_voltage, max_amperage, serial_number,
                manufacturer, model, installation_date, last_maintenance_date,
                created_by, updated_by, created_at, updated_at
            FROM connectors 
            WHERE connector_id = $1
            "#,
            id.0
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let status = match record.status.as_str() {
                    "available" => ConnectorStatus::Available,
                    "occupied" => ConnectorStatus::Occupied,
                    "out_of_service" => ConnectorStatus::OutOfService,
                    "reserved" => ConnectorStatus::Reserved,
                    _ => return Err(RepositoryError::DatabaseError("Invalid connector status".to_string())),
                };

                let power_level_kw = PowerKW::new(record.power_level_kw)
                    .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

                Ok(Some(Connector {
                    id: ConnectorId(record.connector_id),
                    station_id: StationId(record.station_id),
                    connector_type_id: ConnectorTypeId(record.connector_type_id),
                    power_level_kw,
                    status,
                    max_voltage: record.max_voltage,
                    max_amperage: record.max_amperage,
                    serial_number: record.serial_number,
                    manufacturer: record.manufacturer,
                    model: record.model,
                    installation_date: record.installation_date,
                    last_maintenance_date: record.last_maintenance_date,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn find_by_station_id(&self, station_id: StationId) -> RepositoryResult<Vec<Connector>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                connector_id, station_id, connector_type_id, power_level_kw, 
                status as "status!: String", max_voltage, max_amperage, serial_number,
                manufacturer, model, installation_date, last_maintenance_date,
                created_by, updated_by, created_at, updated_at
            FROM connectors
            WHERE station_id = $1
            ORDER BY connector_id
            "#,
            station_id.0
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let connectors = records
            .into_iter()
            .map(|record| {
                let status = match record.status.as_str() {
                    "available" => ConnectorStatus::Available,
                    "occupied" => ConnectorStatus::Occupied,
                    "out_of_service" => ConnectorStatus::OutOfService,
                    "reserved" => ConnectorStatus::Reserved,
                    _ => panic!("Invalid connector status in database"),
                };

                let power_level_kw = PowerKW::new(record.power_level_kw)
                    .expect("Invalid power level in database");

                Connector {
                    id: ConnectorId(record.connector_id),
                    station_id: StationId(record.station_id),
                    connector_type_id: ConnectorTypeId(record.connector_type_id),
                    power_level_kw,
                    status,
                    max_voltage: record.max_voltage,
                    max_amperage: record.max_amperage,
                    serial_number: record.serial_number,
                    manufacturer: record.manufacturer,
                    model: record.model,
                    installation_date: record.installation_date,
                    last_maintenance_date: record.last_maintenance_date,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(connectors)
    }

    async fn find_available_by_station_id(&self, station_id: StationId) -> RepositoryResult<Vec<Connector>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                connector_id, station_id, connector_type_id, power_level_kw, 
                status as "status!: String", max_voltage, max_amperage, serial_number,
                manufacturer, model, installation_date, last_maintenance_date,
                created_by, updated_by, created_at, updated_at
            FROM connectors
            WHERE station_id = $1 AND status = 'available'
            ORDER BY connector_id
            "#,
            station_id.0
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let connectors = records
            .into_iter()
            .map(|record| {
                let status = match record.status.as_str() {
                    "available" => ConnectorStatus::Available,
                    _ => panic!("Expected available status in database"),
                };

                let power_level_kw = PowerKW::new(record.power_level_kw)
                    .expect("Invalid power level in database");

                Connector {
                    id: ConnectorId(record.connector_id),
                    station_id: StationId(record.station_id),
                    connector_type_id: ConnectorTypeId(record.connector_type_id),
                    power_level_kw,
                    status,
                    max_voltage: record.max_voltage,
                    max_amperage: record.max_amperage,
                    serial_number: record.serial_number,
                    manufacturer: record.manufacturer,
                    model: record.model,
                    installation_date: record.installation_date,
                    last_maintenance_date: record.last_maintenance_date,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(connectors)
    }

    async fn find_by_status(&self, status: ConnectorStatus) -> RepositoryResult<Vec<Connector>> {
        let status_str = match status {
            ConnectorStatus::Available => "available",
            ConnectorStatus::Occupied => "occupied",
            ConnectorStatus::OutOfService => "out_of_service",
            ConnectorStatus::Reserved => "reserved",
        };

        let records = sqlx::query!(
            r#"
            SELECT 
                connector_id, station_id, connector_type_id, power_level_kw, 
                status as "status!: String", max_voltage, max_amperage, serial_number,
                manufacturer, model, installation_date, last_maintenance_date,
                created_by, updated_by, created_at, updated_at
            FROM connectors
            WHERE status = $1
            ORDER BY connector_id
            "#,
            status_str
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let connectors = records
            .into_iter()
            .map(|record| {
                let status = match record.status.as_str() {
                    "available" => ConnectorStatus::Available,
                    "occupied" => ConnectorStatus::Occupied,
                    "out_of_service" => ConnectorStatus::OutOfService,
                    "reserved" => ConnectorStatus::Reserved,
                    _ => panic!("Invalid connector status in database"),
                };

                let power_level_kw = PowerKW::new(record.power_level_kw)
                    .expect("Invalid power level in database");

                Connector {
                    id: ConnectorId(record.connector_id),
                    station_id: StationId(record.station_id),
                    connector_type_id: ConnectorTypeId(record.connector_type_id),
                    power_level_kw,
                    status,
                    max_voltage: record.max_voltage,
                    max_amperage: record.max_amperage,
                    serial_number: record.serial_number,
                    manufacturer: record.manufacturer,
                    model: record.model,
                    installation_date: record.installation_date,
                    last_maintenance_date: record.last_maintenance_date,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(connectors)
    }

    async fn save(&self, connector: &mut Connector) -> RepositoryResult<()> {
        let status_str = match connector.status {
            ConnectorStatus::Available => "available",
            ConnectorStatus::Occupied => "occupied",
            ConnectorStatus::OutOfService => "out_of_service",
            ConnectorStatus::Reserved => "reserved",
        };

        if connector.id.0 == 0 {
            // Insert new connector
            let result = sqlx::query!(
                r#"
                INSERT INTO connectors (
                    station_id, connector_type_id, power_level_kw, status, max_voltage, max_amperage,
                    serial_number, manufacturer, model, installation_date, last_maintenance_date,
                    created_by, updated_by
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
                RETURNING connector_id, created_at, updated_at
                "#,
                connector.station_id.0,
                connector.connector_type_id.0,
                connector.power_level_kw.0,
                status_str,
                connector.max_voltage,
                connector.max_amperage,
                connector.serial_number,
                connector.manufacturer,
                connector.model,
                connector.installation_date,
                connector.last_maintenance_date,
                Uuid::from(connector.created_by.0),
                connector.updated_by.map(|user_id| Uuid::from(user_id.0))
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            connector.id = ConnectorId(result.connector_id);
            connector.created_at = result.created_at;
            connector.updated_at = result.updated_at;
        } else {
            // Update existing connector
            let result = sqlx::query!(
                r#"
                UPDATE connectors 
                SET station_id = $1, connector_type_id = $2, power_level_kw = $3, status = $4,
                    max_voltage = $5, max_amperage = $6, serial_number = $7, manufacturer = $8,
                    model = $9, installation_date = $10, last_maintenance_date = $11,
                    updated_by = $12, updated_at = CURRENT_TIMESTAMP
                WHERE connector_id = $13
                RETURNING updated_at
                "#,
                connector.station_id.0,
                connector.connector_type_id.0,
                connector.power_level_kw.0,
                status_str,
                connector.max_voltage,
                connector.max_amperage,
                connector.serial_number,
                connector.manufacturer,
                connector.model,
                connector.installation_date,
                connector.last_maintenance_date,
                connector.updated_by.map(|user_id| Uuid::from(user_id.0)),
                connector.id.0
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            connector.updated_at = result.updated_at;
        }

        Ok(())
    }

    async fn delete(&self, id: ConnectorId) -> RepositoryResult<()> {
        let rows_affected = sqlx::query!(
            "DELETE FROM connectors WHERE connector_id = $1",
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