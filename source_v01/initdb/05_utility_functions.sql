-- Function to find nearby stations
-- Drop and recreate the function with proper parameter types
CREATE OR REPLACE FUNCTION find_nearby_stations(
    p_latitude FLOAT,
    p_longitude FLOAT,
    p_radius_meters INTEGER DEFAULT 5000,
    p_limit INTEGER DEFAULT 50
) RETURNS TABLE(
    id BIGINT,
    name VARCHAR,
    address TEXT,
    distance_meters FLOAT,
    has_available_connectors BOOLEAN,
    total_available_connectors BIGINT,
    max_power_kw DECIMAL,
    power_tier TEXT,
    operator TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        gs.id,
        gs.name,
        gs.address,
        ST_Distance(gs.location, ST_Point(p_longitude, p_latitude)::GEOGRAPHY) as distance_meters,
        gs.has_available_connectors,
        gs.total_available_connectors,
        gs.max_power_kw,
        gs.power_tier,
        gs.operator
    FROM mv_charging_stations_geo gs
    WHERE ST_DWithin(gs.location, ST_Point(p_longitude, p_latitude)::GEOGRAPHY, p_radius_meters)
    ORDER BY ST_Distance(gs.location, ST_Point(p_longitude, p_latitude)::GEOGRAPHY)
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- Function to export data for map clients
CREATE OR REPLACE FUNCTION export_stations_geojson()
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(
            json_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(location::geometry)::json,
                'properties', json_build_object(
                    'id', id,
                    'osm_id', osm_id,
                    'name', name,
                    'address', address,
                    'max_power_kw', max_power_kw,
                    'total_available_connectors', total_available_connectors,
                    'total_connectors', total_connectors,
                    'operator', operator,
                    'opening_hours', opening_hours,
                    'capacity', capacity,
                    'fee', fee,
                    'parking_fee', parking_fee,
                    'access', access,
                    'power_tier', power_tier,
                    'has_available_connectors', has_available_connectors,
                    'available_connector_names', available_connector_names
                )
            )
        )
    ) INTO result
    FROM mv_charging_stations_geo;

    RETURN result;
END;
$$ LANGUAGE plpgsql;


-- Create the missing functions
CREATE OR REPLACE FUNCTION get_station_statistics()
RETURNS TABLE(
    total_stations BIGINT,
    total_connectors BIGINT,
    available_connectors BIGINT,
    avg_power_kw NUMERIC,
    stations_with_available BIGINT,
    connector_type_breakdown JSON
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(DISTINCT cs.id) as total_stations,
        COALESCE(SUM(sc.count_total), 0) as total_connectors,
        COALESCE(SUM(sc.count_available), 0) as available_connectors,
        AVG(sc.power_kw) as avg_power_kw,
        COUNT(DISTINCT CASE WHEN EXISTS (
            SELECT 1 FROM station_connectors sc2 
            WHERE sc2.station_id = cs.id AND sc2.count_available > 0
        ) THEN cs.id END) as stations_with_available,
        (
            SELECT json_agg(row_to_json(t))
            FROM (
                SELECT 
                    ct.name as connector_type,
                    COUNT(sc.id) as count,
                    SUM(sc.count_available) as available,
                    AVG(sc.power_kw) as avg_power
                FROM station_connectors sc
                JOIN connector_types ct ON sc.connector_type_id = ct.id
                GROUP BY ct.name
                ORDER BY count DESC
            ) t
        ) as connector_type_breakdown
    FROM charging_stations cs
    LEFT JOIN station_connectors sc ON cs.id = sc.station_id;
END;
$$ LANGUAGE plpgsql;

-- Create GeoJSON export function
CREATE OR REPLACE FUNCTION export_stations_geojson()
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
    SELECT json_build_object(
        'type', 'FeatureCollection',
        'features', json_agg(
            json_build_object(
                'type', 'Feature',
                'geometry', ST_AsGeoJSON(location::geometry)::json,
                'properties', json_build_object(
                    'id', id,
                    'osm_id', osm_id,
                    'name', name,
                    'address', address,
                    'max_power_kw', max_power_kw,
                    'total_available_connectors', total_available_connectors,
                    'total_connectors', total_connectors,
                    'operator', operator,
                    'opening_hours', opening_hours,
                    'capacity', capacity,
                    'fee', fee,
                    'parking_fee', parking_fee,
                    'access', access,
                    'power_tier', power_tier,
                    'has_available_connectors', has_available_connectors
                )
            )
        )
    ) INTO result
    FROM mv_charging_stations_geo;

    RETURN COALESCE(result, '{"type":"FeatureCollection","features":[]}'::json);
END;
$$ LANGUAGE plpgsql;