-- Create OSM staging table
CREATE TABLE IF NOT EXISTS osm_charging_stations_temp (
    osm_id BIGINT PRIMARY KEY,
    name VARCHAR(255),
    address TEXT,
    longitude FLOAT,
    latitude FLOAT,
    operator VARCHAR(255),
    opening_hours TEXT,
    capacity INTEGER,
    fee TEXT,
    parking_fee TEXT,
    access TEXT,
    socket_type2 INTEGER,
    socket_ccs INTEGER,
    socket_chademo INTEGER,
    socket_type2_output DECIMAL(5,2),
    socket_ccs_output DECIMAL(5,2),
    socket_chademo_output DECIMAL(5,2),
    tags HSTORE,
    geom GEOMETRY(Point, 4326),
    imported_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_osm_temp_geom ON osm_charging_stations_temp USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_osm_temp_osm_id ON osm_charging_stations_temp (osm_id);

-- Function to extract connectors from OSM tags
CREATE OR REPLACE FUNCTION extract_connectors_from_osm_tags(
    p_station_id BIGINT, 
    p_tags HSTORE, 
    p_user_id INTEGER
) RETURNS INTEGER AS $$
DECLARE
    v_connector_count INTEGER := 0;
    v_count_total INTEGER;
    v_power_kw DECIMAL(5,2);
BEGIN
    -- Clear existing connectors for this station
    DELETE FROM station_connectors WHERE station_id = p_station_id;
    
    -- Insert Type2 connectors
    IF p_tags ? 'socket:type2' AND p_tags->'socket:type2' ~ '^\d+$' THEN
        v_count_total := (p_tags->'socket:type2')::INTEGER;
        v_power_kw := NULLIF(p_tags->'socket:type2:output', '')::DECIMAL;
        
        INSERT INTO station_connectors (
            station_id, connector_type_id, status_id, current_type_id,
            power_kw, count_total, count_available, created_by, created_at
        ) VALUES (
            p_station_id,
            (SELECT id FROM connector_types WHERE name = 'type2'),
            1,  -- Available
            (SELECT id FROM current_types WHERE name = 'AC'),
            COALESCE(v_power_kw, 22.0),
            v_count_total,
            v_count_total,  -- Assume all available initially
            p_user_id,
            NOW()
        );
        v_connector_count := v_connector_count + 1;
    END IF;
    
    -- Insert CCS connectors
    IF p_tags ? 'socket:ccs' AND p_tags->'socket:ccs' ~ '^\d+$' THEN
        v_count_total := (p_tags->'socket:ccs')::INTEGER;
        v_power_kw := NULLIF(p_tags->'socket:ccs:output', '')::DECIMAL;
        
        INSERT INTO station_connectors (
            station_id, connector_type_id, status_id, current_type_id,
            power_kw, count_total, count_available, created_by, created_at
        ) VALUES (
            p_station_id,
            (SELECT id FROM connector_types WHERE name = 'ccs'),
            1,  -- Available
            (SELECT id FROM current_types WHERE name = 'DC'),
            COALESCE(v_power_kw, 50.0),
            v_count_total,
            v_count_total,
            p_user_id,
            NOW()
        );
        v_connector_count := v_connector_count + 1;
    END IF;
    
    -- Insert CHAdeMO connectors
    IF p_tags ? 'socket:chademo' AND p_tags->'socket:chademo' ~ '^\d+$' THEN
        v_count_total := (p_tags->'socket:chademo')::INTEGER;
        v_power_kw := NULLIF(p_tags->'socket:chademo:output', '')::DECIMAL;
        
        INSERT INTO station_connectors (
            station_id, connector_type_id, status_id, current_type_id,
            power_kw, count_total, count_available, created_by, created_at
        ) VALUES (
            p_station_id,
            (SELECT id FROM connector_types WHERE name = 'chademo'),
            1,  -- Available
            (SELECT id FROM current_types WHERE name = 'DC'),
            COALESCE(v_power_kw, 50.0),
            v_count_total,
            v_count_total,
            p_user_id,
            NOW()
        );
        v_connector_count := v_connector_count + 1;
    END IF;

    RETURN v_connector_count;
END;
$$ LANGUAGE plpgsql;

-- Main OSM sync function
CREATE OR REPLACE FUNCTION sync_osm_charging_stations(
    p_user_id INTEGER DEFAULT 1
) RETURNS TABLE(
    updated_count INTEGER,
    inserted_count INTEGER,
    deactivated_count INTEGER
) AS $$
DECLARE
    v_updated_count INTEGER := 0;
    v_inserted_count INTEGER := 0;
    v_deactivated_count INTEGER := 0;
    v_station_id BIGINT;
    v_tags HSTORE;
BEGIN
    -- Update existing stations
    WITH updated AS (
        UPDATE charging_stations cs
        SET 
            name = COALESCE(osm.name, cs.name),
            address = COALESCE(osm.address, cs.address),
            tags = cs.tags || hstore(array[
                ['operator', osm.operator],
                ['opening_hours', osm.opening_hours],
                ['capacity', osm.capacity::text],
                ['fee', osm.fee],
                ['parking_fee', osm.parking_fee],
                ['access', osm.access],
                ['socket:type2', osm.socket_type2::text],
                ['socket:ccs', osm.socket_ccs::text],
                ['socket:chademo', osm.socket_chademo::text],
                ['socket:type2:output', osm.socket_type2_output::text],
                ['socket:ccs:output', osm.socket_ccs_output::text],
                ['socket:chademo:output', osm.socket_chademo_output::text]
            ]) || osm.tags,
            updated_by = p_user_id,
            updated_at = NOW()
        FROM osm_charging_stations_temp osm
        WHERE cs.osm_id = osm.osm_id
        AND (
            cs.name IS DISTINCT FROM osm.name OR
            cs.address IS DISTINCT FROM osm.address OR
            cs.tags IS DISTINCT FROM (
                hstore(array[
                    ['operator', osm.operator],
                    ['opening_hours', osm.opening_hours],
                    ['capacity', osm.capacity::text],
                    ['fee', osm.fee],
                    ['parking_fee', osm.parking_fee],
                    ['access', osm.access],
                    ['socket:type2', osm.socket_type2::text],
                    ['socket:ccs', osm.socket_ccs::text],
                    ['socket:chademo', osm.socket_chademo::text],
                    ['socket:type2:output', osm.socket_type2_output::text],
                    ['socket:ccs:output', osm.socket_ccs_output::text],
                    ['socket:chademo:output', osm.socket_chademo_output::text]
                ]) || osm.tags
            )
        )
        RETURNING cs.id, cs.tags
    )
    SELECT COUNT(*) INTO v_updated_count FROM updated;

    -- Process connectors for updated stations
    FOR v_station_id, v_tags IN 
        SELECT cs.id, cs.tags 
        FROM charging_stations cs
        INNER JOIN osm_charging_stations_temp osm ON cs.osm_id = osm.osm_id
        WHERE cs.updated_at >= NOW() - INTERVAL '5 minutes'
    LOOP
        PERFORM extract_connectors_from_osm_tags(v_station_id, v_tags, p_user_id);
    END LOOP;

    -- Insert new stations
    WITH inserted AS (
        INSERT INTO charging_stations (
            osm_id, name, address, location, tags, created_by, created_at
        )
        SELECT 
            osm.osm_id,
            osm.name,
            osm.address,
            osm.geom::GEOGRAPHY,
            hstore(array[
                ['operator', osm.operator],
                ['opening_hours', osm.opening_hours],
                ['capacity', osm.capacity::text],
                ['fee', osm.fee],
                ['parking_fee', osm.parking_fee],
                ['access', osm.access],
                ['socket:type2', osm.socket_type2::text],
                ['socket:ccs', osm.socket_ccs::text],
                ['socket:chademo', osm.socket_chademo::text],
                ['socket:type2:output', osm.socket_type2_output::text],
                ['socket:ccs:output', osm.socket_ccs_output::text],
                ['socket:chademo:output', osm.socket_chademo_output::text]
            ]) || osm.tags,
            p_user_id,
            NOW()
        FROM osm_charging_stations_temp osm
        WHERE NOT EXISTS (
            SELECT 1 FROM charging_stations WHERE osm_id = osm.osm_id
        )
        RETURNING id, osm_id, tags
    )
    SELECT COUNT(*) INTO v_inserted_count FROM inserted;

    -- Process connectors for new stations
    FOR v_station_id, v_tags IN 
        SELECT cs.id, cs.tags 
        FROM charging_stations cs
        INNER JOIN osm_charging_stations_temp osm ON cs.osm_id = osm.osm_id
        WHERE cs.created_at >= NOW() - INTERVAL '5 minutes'
    LOOP
        PERFORM extract_connectors_from_osm_tags(v_station_id, v_tags, p_user_id);
    END LOOP;

    -- Refresh materialized views if there were changes
    IF (v_updated_count + v_inserted_count) > 0 THEN
        PERFORM refresh_charging_station_views();
    END IF;

    RETURN QUERY SELECT v_updated_count, v_inserted_count, v_deactivated_count;

EXCEPTION WHEN OTHERS THEN
    RAISE EXCEPTION 'OSM sync failed: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- View refresh function
CREATE OR REPLACE FUNCTION refresh_charging_station_views()
RETURNS VOID AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_charging_stations_geo;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_charging_stations_summary;
    REFRESH MATERIALIZED VIEW CONCURRENTLY mv_connector_type_stats;
END;
$$ LANGUAGE plpgsql;

-- Function to get current user ID (placeholder)
CREATE OR REPLACE FUNCTION current_user_id()
RETURNS INTEGER AS $$
BEGIN
    RETURN 1;  -- Replace with actual user ID logic
END;
$$ LANGUAGE plpgsql;

-- Trigger function for updated timestamps
CREATE OR REPLACE FUNCTION update_charging_station_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_by := current_user_id();
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers
CREATE TRIGGER update_charging_station_timestamp_trigger
    BEFORE UPDATE ON charging_stations
    FOR EACH ROW
    EXECUTE FUNCTION update_charging_station_timestamp();

CREATE TRIGGER update_station_connectors_timestamp_trigger
    BEFORE UPDATE ON station_connectors
    FOR EACH ROW
    EXECUTE FUNCTION update_charging_station_timestamp();