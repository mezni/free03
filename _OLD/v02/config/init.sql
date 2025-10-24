CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS hstore;

-- Charging stations table
CREATE TABLE charging_stations (
    id BIGSERIAL PRIMARY KEY,
    osm_id BIGINT, -- Reference to OSM node/way ID
    name VARCHAR(255) NOT NULL,
    operator VARCHAR(255),
    address TEXT,
    
    -- Location (PostGIS geometry)
    location GEOGRAPHY(Point, 4326)
);