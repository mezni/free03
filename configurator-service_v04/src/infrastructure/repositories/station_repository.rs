use async_trait::async_trait;
use sqlx::{PgPool, Row};
use chrono::{DateTime, Utc};
use uuid::Uuid;

use crate::domain::models::Station;
use crate::domain::repositories::{StationRepository, RepositoryResult, RepositoryError};
use crate::domain::value_objects::{StationId, NetworkId, Location, OsmId, UserId, Tags};

pub struct StationRepositoryImpl {
    pool: PgPool,
}

impl StationRepositoryImpl {
    pub fn new(pool: PgPool) -> Self {
        Self { pool }
    }
}

#[async_trait]
impl StationRepository for StationRepositoryImpl {
    async fn find_by_id(&self, id: StationId) -> RepositoryResult<Option<Station>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                station_id, network_id, name, address, city, state, country, postal_code,
                ST_X(location::geometry) as longitude, ST_Y(location::geometry) as latitude,
                tags, osm_id, is_operational, created_by, updated_by, created_at, updated_at
            FROM stations 
            WHERE station_id = $1
            "#,
            id.0
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let location = Location::new(record.latitude, record.longitude)
                    .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

                let tags: Tags = record.tags
                    .map(|hstore| {
                        hstore.into_iter()
                            .map(|(k, v)| (k.unwrap_or_default(), v.unwrap_or_default()))
                            .collect()
                    })
                    .unwrap_or_default();

                Ok(Some(Station {
                    id: StationId(record.station_id),
                    network_id: NetworkId(record.network_id),
                    name: record.name,
                    address: record.address,
                    city: record.city,
                    state: record.state,
                    country: record.country,
                    postal_code: record.postal_code,
                    location,
                    tags,
                    osm_id: record.osm_id.map(OsmId),
                    is_operational: record.is_operational,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn find_by_network_id(&self, network_id: NetworkId) -> RepositoryResult<Vec<Station>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                station_id, network_id, name, address, city, state, country, postal_code,
                ST_X(location::geometry) as longitude, ST_Y(location::geometry) as latitude,
                tags, osm_id, is_operational, created_by, updated_by, created_at, updated_at
            FROM stations
            WHERE network_id = $1
            ORDER BY name
            "#,
            network_id.0
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let stations = records
            .into_iter()
            .map(|record| {
                let location = Location::new(record.latitude, record.longitude)
                    .expect("Invalid location in database");

                let tags: Tags = record.tags
                    .map(|hstore| {
                        hstore.into_iter()
                            .map(|(k, v)| (k.unwrap_or_default(), v.unwrap_or_default()))
                            .collect()
                    })
                    .unwrap_or_default();

                Station {
                    id: StationId(record.station_id),
                    network_id: NetworkId(record.network_id),
                    name: record.name,
                    address: record.address,
                    city: record.city,
                    state: record.state,
                    country: record.country,
                    postal_code: record.postal_code,
                    location,
                    tags,
                    osm_id: record.osm_id.map(OsmId),
                    is_operational: record.is_operational,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(stations)
    }

    async fn find_by_location(
        &self,
        latitude: f64,
        longitude: f64,
        radius_km: f64,
    ) -> RepositoryResult<Vec<Station>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                station_id, network_id, name, address, city, state, country, postal_code,
                ST_X(location::geometry) as longitude, ST_Y(location::geometry) as latitude,
                tags, osm_id, is_operational, created_by, updated_by, created_at, updated_at,
                ST_Distance(location, ST_SetSRID(ST_MakePoint($1, $2), 4326)) as distance
            FROM stations
            WHERE ST_DWithin(location, ST_SetSRID(ST_MakePoint($1, $2), 4326), $3)
            AND is_operational = true
            ORDER BY distance
            "#,
            longitude,
            latitude,
            radius_km * 1000.0 // Convert km to meters
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let stations = records
            .into_iter()
            .map(|record| {
                let location = Location::new(record.latitude, record.longitude)
                    .expect("Invalid location in database");

                let tags: Tags = record.tags
                    .map(|hstore| {
                        hstore.into_iter()
                            .map(|(k, v)| (k.unwrap_or_default(), v.unwrap_or_default()))
                            .collect()
                    })
                    .unwrap_or_default();

                Station {
                    id: StationId(record.station_id),
                    network_id: NetworkId(record.network_id),
                    name: record.name,
                    address: record.address,
                    city: record.city,
                    state: record.state,
                    country: record.country,
                    postal_code: record.postal_code,
                    location,
                    tags,
                    osm_id: record.osm_id.map(OsmId),
                    is_operational: record.is_operational,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(stations)
    }

    async fn find_by_osm_id(&self, osm_id: OsmId) -> RepositoryResult<Option<Station>> {
        let result = sqlx::query!(
            r#"
            SELECT 
                station_id, network_id, name, address, city, state, country, postal_code,
                ST_X(location::geometry) as longitude, ST_Y(location::geometry) as latitude,
                tags, osm_id, is_operational, created_by, updated_by, created_at, updated_at
            FROM stations 
            WHERE osm_id = $1
            "#,
            osm_id.0
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        match result {
            Some(record) => {
                let location = Location::new(record.latitude, record.longitude)
                    .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

                let tags: Tags = record.tags
                    .map(|hstore| {
                        hstore.into_iter()
                            .map(|(k, v)| (k.unwrap_or_default(), v.unwrap_or_default()))
                            .collect()
                    })
                    .unwrap_or_default();

                Ok(Some(Station {
                    id: StationId(record.station_id),
                    network_id: NetworkId(record.network_id),
                    name: record.name,
                    address: record.address,
                    city: record.city,
                    state: record.state,
                    country: record.country,
                    postal_code: record.postal_code,
                    location,
                    tags,
                    osm_id: record.osm_id.map(OsmId),
                    is_operational: record.is_operational,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }))
            }
            None => Ok(None),
        }
    }

    async fn save(&self, station: &mut Station) -> RepositoryResult<()> {
        let tags: std::collections::HashMap<String, Option<String>> = station.tags
            .iter()
            .map(|(k, v)| (k.clone(), Some(v.clone())))
            .collect();

        if station.id.0 == 0 {
            // Insert new station
            let result = sqlx::query!(
                r#"
                INSERT INTO stations (
                    network_id, name, address, city, state, country, postal_code, location,
                    tags, osm_id, is_operational, created_by, updated_by
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, ST_SetSRID(ST_MakePoint($8, $9), 4326), $10, $11, $12, $13, $14)
                RETURNING station_id, created_at, updated_at
                "#,
                station.network_id.0,
                station.name,
                station.address,
                station.city,
                station.state,
                station.country,
                station.postal_code,
                station.location.longitude,
                station.location.latitude,
                tags,
                station.osm_id.map(|id| id.0),
                station.is_operational,
                Uuid::from(station.created_by.0),
                station.updated_by.map(|user_id| Uuid::from(user_id.0))
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            station.id = StationId(result.station_id);
            station.created_at = result.created_at;
            station.updated_at = result.updated_at;
        } else {
            // Update existing station
            let result = sqlx::query!(
                r#"
                UPDATE stations 
                SET name = $1, address = $2, city = $3, state = $4, country = $5, postal_code = $6,
                    location = ST_SetSRID(ST_MakePoint($7, $8), 4326), tags = $9, osm_id = $10,
                    is_operational = $11, updated_by = $12, updated_at = CURRENT_TIMESTAMP
                WHERE station_id = $13
                RETURNING updated_at
                "#,
                station.name,
                station.address,
                station.city,
                station.state,
                station.country,
                station.postal_code,
                station.location.longitude,
                station.location.latitude,
                tags,
                station.osm_id.map(|id| id.0),
                station.is_operational,
                station.updated_by.map(|user_id| Uuid::from(user_id.0)),
                station.id.0
            )
            .fetch_one(&self.pool)
            .await
            .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

            station.updated_at = result.updated_at;
        }

        Ok(())
    }

    async fn delete(&self, id: StationId) -> RepositoryResult<()> {
        let rows_affected = sqlx::query!(
            "DELETE FROM stations WHERE station_id = $1",
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

    async fn find_operational_stations(&self) -> RepositoryResult<Vec<Station>> {
        let records = sqlx::query!(
            r#"
            SELECT 
                station_id, network_id, name, address, city, state, country, postal_code,
                ST_X(location::geometry) as longitude, ST_Y(location::geometry) as latitude,
                tags, osm_id, is_operational, created_by, updated_by, created_at, updated_at
            FROM stations
            WHERE is_operational = true
            ORDER BY name
            "#
        )
        .fetch_all(&self.pool)
        .await
        .map_err(|e| RepositoryError::DatabaseError(e.to_string()))?;

        let stations = records
            .into_iter()
            .map(|record| {
                let location = Location::new(record.latitude, record.longitude)
                    .expect("Invalid location in database");

                let tags: Tags = record.tags
                    .map(|hstore| {
                        hstore.into_iter()
                            .map(|(k, v)| (k.unwrap_or_default(), v.unwrap_or_default()))
                            .collect()
                    })
                    .unwrap_or_default();

                Station {
                    id: StationId(record.station_id),
                    network_id: NetworkId(record.network_id),
                    name: record.name,
                    address: record.address,
                    city: record.city,
                    state: record.state,
                    country: record.country,
                    postal_code: record.postal_code,
                    location,
                    tags,
                    osm_id: record.osm_id.map(OsmId),
                    is_operational: record.is_operational,
                    created_by: UserId::parse_str(&record.created_by.to_string()).unwrap(),
                    updated_by: record.updated_by.map(|uuid| UserId::parse_str(&uuid.to_string()).unwrap()),
                    created_at: record.created_at,
                    updated_at: record.updated_at,
                }
            })
            .collect();

        Ok(stations)
    }
}