use crate::domain::entities::stations::{Point, Station};
use crate::domain::repositories::StationRepository;
use crate::shared::errors::AppError;
use async_trait::async_trait;
use chrono::{DateTime, Utc};
use sqlx::PgPool;
use sqlx::postgres::types::PgHstore;
use std::collections::HashMap;

#[derive(Debug, Clone)]
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
    async fn find_by_id(&self, station_id: i32) -> Result<Option<Station>, AppError> {
        let record = sqlx::query!(
            r#"
            SELECT station_id, network_id, name, address, city, state, country, postal_code,
                   ST_X(location::geometry) as longitude, ST_Y(location::geometry) as latitude,
                   tags, osm_id, is_operational, created_by, updated_by, created_at, updated_at
            FROM stations 
            WHERE station_id = $1
            "#,
            station_id
        )
        .fetch_optional(&self.pool)
        .await?;

        let station = record.map(|r| {
            let location = Point {
                longitude: r.longitude.unwrap_or(0.0),
                latitude: r.latitude.unwrap_or(0.0),
            };

            let tags = parse_hstore(&r.tags);

            Station {
                station_id: r.station_id,
                network_id: r.network_id,
                name: r.name,
                address: r.address,
                city: r.city,
                state: r.state,
                country: r.country,
                postal_code: r.postal_code,
                location,
                tags,
                osm_id: r.osm_id,
                is_operational: r.is_operational.unwrap_or(true),
                created_by: r.created_by,
                updated_by: r.updated_by,
                created_at: DateTime::from_naive_utc_and_offset(
                    r.created_at.unwrap_or_default(),
                    Utc,
                ),
                updated_at: DateTime::from_naive_utc_and_offset(
                    r.updated_at.unwrap_or_default(),
                    Utc,
                ),
            }
        });

        Ok(station)
    }

    async fn find_by_network_id(
        &self,
        network_id: i32,
        page: u32,
        page_size: u32,
    ) -> Result<Vec<Station>, AppError> {
        let offset = (page - 1) * page_size;

        let records = sqlx::query!(
            r#"
            SELECT station_id, network_id, name, address, city, state, country, postal_code,
                   ST_X(location::geometry) as longitude, ST_Y(location::geometry) as latitude,
                   tags, osm_id, is_operational, created_by, updated_by, created_at, updated_at
            FROM stations 
            WHERE network_id = $1
            ORDER BY created_at DESC
            LIMIT $2 OFFSET $3
            "#,
            network_id,
            page_size as i64,
            offset as i64
        )
        .fetch_all(&self.pool)
        .await?;

        let stations = records
            .into_iter()
            .map(|r| {
                let location = Point {
                    longitude: r.longitude.unwrap_or(0.0),
                    latitude: r.latitude.unwrap_or(0.0),
                };

                let tags = parse_hstore(&r.tags);

                Station {
                    station_id: r.station_id,
                    network_id: r.network_id,
                    name: r.name,
                    address: r.address,
                    city: r.city,
                    state: r.state,
                    country: r.country,
                    postal_code: r.postal_code,
                    location,
                    tags,
                    osm_id: r.osm_id,
                    is_operational: r.is_operational.unwrap_or(true),
                    created_by: r.created_by,
                    updated_by: r.updated_by,
                    created_at: DateTime::from_naive_utc_and_offset(
                        r.created_at.unwrap_or_default(),
                        Utc,
                    ),
                    updated_at: DateTime::from_naive_utc_and_offset(
                        r.updated_at.unwrap_or_default(),
                        Utc,
                    ),
                }
            })
            .collect();

        Ok(stations)
    }

    async fn save(&self, station: &Station) -> Result<Station, AppError> {
        let tags_hstore = station.tags.as_ref().map(|map| {
            PgHstore(
                map.iter()
                    .map(|(k, v)| (k.clone(), Some(v.clone())))
                    .collect(),
            )
        });

        let saved_station = if station.station_id == 0 {
            let record = sqlx::query!(
                r#"
                INSERT INTO stations (network_id, name, address, city, state, country, postal_code, 
                                    location, tags, osm_id, is_operational, created_by, updated_by)
                VALUES ($1, $2, $3, $4, $5, $6, $7, ST_GeogFromText($8), $9, $10, $11, $12, $13)
                RETURNING station_id, network_id, name, address, city, state, country, postal_code,
                          ST_X(location::geometry) as longitude, ST_Y(location::geometry) as latitude,
                          tags, osm_id, is_operational, created_by, updated_by, created_at, updated_at
                "#,
                station.network_id,
                station.name,
                station.address,
                station.city,
                station.state,
                station.country,
                station.postal_code,
                station.location.to_wkt(),
                tags_hstore,
                station.osm_id,
                station.is_operational,
                station.created_by,
                station.updated_by
            )
            .fetch_one(&self.pool)
            .await?;

            let location = Point {
                longitude: record.longitude.unwrap_or(0.0),
                latitude: record.latitude.unwrap_or(0.0),
            };

            let tags = parse_hstore(&record.tags);

            Station {
                station_id: record.station_id,
                network_id: record.network_id,
                name: record.name,
                address: record.address,
                city: record.city,
                state: record.state,
                country: record.country,
                postal_code: record.postal_code,
                location,
                tags,
                osm_id: record.osm_id,
                is_operational: record.is_operational.unwrap_or(true),
                created_by: record.created_by,
                updated_by: record.updated_by,
                created_at: DateTime::from_naive_utc_and_offset(
                    record.created_at.unwrap_or_default(),
                    Utc,
                ),
                updated_at: DateTime::from_naive_utc_and_offset(
                    record.updated_at.unwrap_or_default(),
                    Utc,
                ),
            }
        } else {
            let record = sqlx::query!(
                r#"
                UPDATE stations 
                SET name = $1, address = $2, city = $3, state = $4, country = $5, postal_code = $6,
                    location = ST_GeogFromText($7), tags = $8, osm_id = $9, is_operational = $10,
                    updated_by = $11, updated_at = CURRENT_TIMESTAMP
                WHERE station_id = $12
                RETURNING station_id, network_id, name, address, city, state, country, postal_code,
                          ST_X(location::geometry) as longitude, ST_Y(location::geometry) as latitude,
                          tags, osm_id, is_operational, created_by, updated_by, created_at, updated_at
                "#,
                station.name,
                station.address,
                station.city,
                station.state,
                station.country,
                station.postal_code,
                station.location.to_wkt(),
                tags_hstore,
                station.osm_id,
                station.is_operational,
                station.updated_by,
                station.station_id
            )
            .fetch_one(&self.pool)
            .await?;

            let location = Point {
                longitude: record.longitude.unwrap_or(0.0),
                latitude: record.latitude.unwrap_or(0.0),
            };

            let tags = parse_hstore(&record.tags);

            Station {
                station_id: record.station_id,
                network_id: record.network_id,
                name: record.name,
                address: record.address,
                city: record.city,
                state: record.state,
                country: record.country,
                postal_code: record.postal_code,
                location,
                tags,
                osm_id: record.osm_id,
                is_operational: record.is_operational.unwrap_or(true),
                created_by: record.created_by,
                updated_by: record.updated_by,
                created_at: DateTime::from_naive_utc_and_offset(
                    record.created_at.unwrap_or_default(),
                    Utc,
                ),
                updated_at: DateTime::from_naive_utc_and_offset(
                    record.updated_at.unwrap_or_default(),
                    Utc,
                ),
            }
        };

        Ok(saved_station)
    }

    async fn delete(&self, station_id: i32) -> Result<(), AppError> {
        let result = sqlx::query!("DELETE FROM stations WHERE station_id = $1", station_id)
            .execute(&self.pool)
            .await?;

        if result.rows_affected() == 0 {
            return Err(AppError::NotFound(format!(
                "Station with id {} not found",
                station_id
            )));
        }

        Ok(())
    }

    async fn find_operational_by_network(&self, network_id: i32) -> Result<Vec<Station>, AppError> {
        let records = sqlx::query!(
            r#"
            SELECT station_id, network_id, name, address, city, state, country, postal_code,
                   ST_X(location::geometry) as longitude, ST_Y(location::geometry) as latitude,
                   tags, osm_id, is_operational, created_by, updated_by, created_at, updated_at
            FROM stations 
            WHERE network_id = $1 AND is_operational = true
            ORDER BY name ASC
            "#,
            network_id
        )
        .fetch_all(&self.pool)
        .await?;

        let stations = records
            .into_iter()
            .map(|r| {
                let location = Point {
                    longitude: r.longitude.unwrap_or(0.0),
                    latitude: r.latitude.unwrap_or(0.0),
                };

                let tags = parse_hstore(&r.tags);

                Station {
                    station_id: r.station_id,
                    network_id: r.network_id,
                    name: r.name,
                    address: r.address,
                    city: r.city,
                    state: r.state,
                    country: r.country,
                    postal_code: r.postal_code,
                    location,
                    tags,
                    osm_id: r.osm_id,
                    is_operational: r.is_operational.unwrap_or(true),
                    created_by: r.created_by,
                    updated_by: r.updated_by,
                    created_at: DateTime::from_naive_utc_and_offset(
                        r.created_at.unwrap_or_default(),
                        Utc,
                    ),
                    updated_at: DateTime::from_naive_utc_and_offset(
                        r.updated_at.unwrap_or_default(),
                        Utc,
                    ),
                }
            })
            .collect();

        Ok(stations)
    }
}

// Helper function: parse PgHstore into HashMap<String, String>
fn parse_hstore(hstore: &Option<PgHstore>) -> Option<HashMap<String, String>> {
    hstore.as_ref().map(|pg| {
        pg.iter()
            .filter_map(|(k, v_opt)| v_opt.as_ref().map(|v| (k.clone(), v.clone())))
            .collect()
    })
}
