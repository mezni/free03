use actix_web::{web, HttpResponse};
use sqlx::{Pool, Postgres, Row};

use crate::models::*;

// Find nearby charging stations
pub async fn find_nearby_stations(
    pool: web::Data<Pool<Postgres>>,
    query: web::Query<NearbyQuery>,
) -> HttpResponse {
    let radius = query.radius.unwrap_or(5000);
    let limit = query.limit.unwrap_or(50);

    let result = sqlx::query_as::<_, NearbyStation>(
        "SELECT * FROM find_nearby_stations($1, $2, $3, $4)"
    )
    .bind(query.lat)
    .bind(query.lng)
    .bind(radius)
    .bind(limit)
    .fetch_all(&**pool)
    .await;

    match result {
        Ok(stations) => HttpResponse::Ok().json(ApiResponse {
            success: true,
            data: Some(stations),
            message: None,
        }),
        Err(e) => {
            eprintln!("Database error: {}", e);
            HttpResponse::InternalServerError().json(ApiResponse::<Vec<NearbyStation>> {
                success: false,
                data: None,
                message: Some("Failed to fetch nearby stations".to_string()),
            })
        }
    }
}

// Get station by ID with detailed information
pub async fn get_station_by_id(
    pool: web::Data<Pool<Postgres>>,
    path: web::Path<i64>,
) -> HttpResponse {
    let station_id = path.into_inner();

    let station_result = sqlx::query_as!(
        ChargingStation,
        r#"
        SELECT 
            id, osm_id, name, address,
            ST_Y(location::geometry) as latitude,
            ST_X(location::geometry) as longitude,
            tags->'operator' as operator,
            tags->'opening_hours' as opening_hours,
            tags->'capacity' as capacity,
            tags->'fee' as fee,
            tags->'parking_fee' as parking_fee,
            tags->'access' as access,
            created_at,
            updated_at
        FROM charging_stations 
        WHERE id = $1
        "#,
        station_id
    )
    .fetch_optional(&**pool)
    .await;

    let connectors_result = sqlx::query(
        r#"
        SELECT 
            sc.id, sc.station_id,
            ct.name as connector_type,
            cs.name as status,
            cur.name as current_type,
            sc.power_kw, sc.voltage, sc.amperage,
            sc.count_available, sc.count_total
        FROM station_connectors sc
        JOIN connector_types ct ON sc.connector_type_id = ct.id
        JOIN connector_statuses cs ON sc.status_id = cs.id
        JOIN current_types cur ON sc.current_type_id = cur.id
        WHERE sc.station_id = $1
        ORDER BY sc.power_kw DESC NULLS LAST
        "#
    )
    .bind(station_id)
    .fetch_all(&**pool)
    .await;

    match (station_result, connectors_result) {
        (Ok(Some(station)), Ok(connectors_rows)) => {
            let connectors: Vec<StationConnector> = connectors_rows.iter().map(|row| {
                StationConnector {
                    id: row.get("id"),
                    station_id: row.get("station_id"),
                    connector_type: row.get("connector_type"),
                    status: row.get("status"),
                    current_type: row.get("current_type"),
                    power_kw: row.get("power_kw"),
                    voltage: row.get("voltage"),
                    amperage: row.get("amperage"),
                    count_available: row.get("count_available"),
                    count_total: row.get("count_total"),
                }
            }).collect();

            let response = serde_json::json!({
                "station": station,
                "connectors": connectors
            });
            HttpResponse::Ok().json(ApiResponse {
                success: true,
                data: Some(response),
                message: None,
            })
        }
        (Ok(None), _) => HttpResponse::NotFound().json(ApiResponse::<serde_json::Value> {
            success: false,
            data: None,
            message: Some("Station not found".to_string()),
        }),
        _ => HttpResponse::InternalServerError().json(ApiResponse::<serde_json::Value> {
            success: false,
            data: None,
            message: Some("Failed to fetch station data".to_string()),
        }),
    }
}

// Keep other handler functions the same as previous version...
// [Include the rest of your handlers from the previous working version]
// Get all stations with pagination
pub async fn get_all_stations(
    pool: web::Data<Pool<Postgres>>,
    query: web::Query<SearchQuery>,
) -> HttpResponse {
    let limit = query.limit.unwrap_or(50) as i64;
    let offset = query.offset.unwrap_or(0) as i64;

    let stations = sqlx::query_as!(
        ChargingStation,
        r#"
        SELECT 
            id, osm_id, name, address,
            ST_Y(location::geometry) as latitude,
            ST_X(location::geometry) as longitude,
            tags->'operator' as operator,
            tags->'opening_hours' as opening_hours,
            tags->'capacity' as capacity,
            tags->'fee' as fee,
            tags->'parking_fee' as parking_fee,
            tags->'access' as access,
            created_at,
            updated_at
        FROM charging_stations 
        ORDER BY created_at DESC
        LIMIT $1 OFFSET $2
        "#,
        limit,
        offset
    )
    .fetch_all(&**pool)
    .await;

    match stations {
        Ok(stations) => HttpResponse::Ok().json(ApiResponse {
            success: true,
            data: Some(stations),
            message: None,
        }),
        Err(e) => {
            eprintln!("Database error: {}", e);
            HttpResponse::InternalServerError().json(ApiResponse::<Vec<ChargingStation>> {
                success: false,
                data: None,
                message: Some("Failed to fetch stations".to_string()),
            })
        }
    }
}

// Search stations by various criteria
pub async fn search_stations(
    pool: web::Data<Pool<Postgres>>,
    query: web::Query<SearchQuery>,
) -> HttpResponse {
    let search_query = query.query.as_deref().unwrap_or("");
    let limit = query.limit.unwrap_or(50) as i64;

    let stations = sqlx::query_as!(
        ChargingStation,
        r#"
        SELECT 
            id, osm_id, name, address,
            ST_Y(location::geometry) as latitude,
            ST_X(location::geometry) as longitude,
            tags->'operator' as operator,
            tags->'opening_hours' as opening_hours,
            tags->'capacity' as capacity,
            tags->'fee' as fee,
            tags->'parking_fee' as parking_fee,
            tags->'access' as access,
            created_at,
            updated_at
        FROM charging_stations 
        WHERE name ILIKE $1 OR address ILIKE $1
        ORDER BY name
        LIMIT $2
        "#,
        format!("%{}%", search_query),
        limit
    )
    .fetch_all(&**pool)
    .await;

    match stations {
        Ok(stations) => HttpResponse::Ok().json(ApiResponse {
            success: true,
            data: Some(stations),
            message: None,
        }),
        Err(e) => {
            eprintln!("Database error: {}", e);
            HttpResponse::InternalServerError().json(ApiResponse::<Vec<ChargingStation>> {
                success: false,
                data: None,
                message: Some("Failed to search stations".to_string()),
            })
        }
    }
}

// Get system statistics
pub async fn get_statistics(pool: web::Data<Pool<Postgres>>) -> HttpResponse {
    let stats = sqlx::query_as!(
        Statistics,
        r#"
        SELECT 
            total_stations,
            total_connectors,
            available_connectors,
            avg_power_kw,
            stations_with_available,
            connector_type_breakdown
        FROM get_station_statistics()
        "#
    )
    .fetch_one(&**pool)
    .await;

    match stats {
        Ok(statistics) => HttpResponse::Ok().json(ApiResponse {
            success: true,
            data: Some(statistics),
            message: None,
        }),
        Err(e) => {
            eprintln!("Database error: {}", e);
            HttpResponse::InternalServerError().json(ApiResponse::<Statistics> {
                success: false,
                data: None,
                message: Some("Failed to fetch statistics".to_string()),
            })
        }
    }
}

// Get all connector types
pub async fn get_connector_types(pool: web::Data<Pool<Postgres>>) -> HttpResponse {
    let connector_types = sqlx::query_as!(
        ConnectorType,
        "SELECT id, name, description FROM connector_types ORDER BY name"
    )
    .fetch_all(&**pool)
    .await;

    match connector_types {
        Ok(types) => HttpResponse::Ok().json(ApiResponse {
            success: true,
            data: Some(types),
            message: None,
        }),
        Err(e) => {
            eprintln!("Database error: {}", e);
            HttpResponse::InternalServerError().json(ApiResponse::<Vec<ConnectorType>> {
                success: false,
                data: None,
                message: Some("Failed to fetch connector types".to_string()),
            })
        }
    }
}

// Export stations as GeoJSON
pub async fn export_geojson(pool: web::Data<Pool<Postgres>>) -> HttpResponse {
    let result = sqlx::query!("SELECT export_stations_geojson() as geojson")
        .fetch_one(&**pool)
        .await;

    match result {
        Ok(record) => {
            if let Some(geojson_data) = record.geojson {
                // Convert JsonValue to String for the response body
                HttpResponse::Ok()
                    .content_type("application/json")
                    .body(geojson_data.to_string())
            } else {
                HttpResponse::InternalServerError().json(ApiResponse::<serde_json::Value> {
                    success: false,
                    data: None,
                    message: Some("Failed to generate GeoJSON".to_string()),
                })
            }
        }
        Err(e) => {
            eprintln!("Database error: {}", e);
            HttpResponse::InternalServerError().json(ApiResponse::<serde_json::Value> {
                success: false,
                data: None,
                message: Some("Failed to export GeoJSON".to_string()),
            })
        }
    }
}