-- Enable PostGIS and other extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS hstore;
CREATE EXTENSION IF NOT EXISTS pgrouting;

-- Charging stations table
CREATE TABLE charging_stations (
    id BIGSERIAL PRIMARY KEY,
    osm_id BIGINT, -- Reference to OSM node/way ID
    name VARCHAR(255) NOT NULL,
    operator VARCHAR(255),
    address TEXT,
    
    -- Location (PostGIS geometry)
    location GEOGRAPHY(Point, 4326),
    
    -- Access information
    access_type VARCHAR(50) CHECK (access_type IN ('public', 'private', 'customers')),
    opening_hours TEXT,
    
    -- Status and metadata
    is_active BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMPTZ DEFAULT NOW(),
    data_source VARCHAR(50) DEFAULT 'osm', -- 'osm', 'user_submitted', 'commercial'
    
    -- Additional OSM tags stored as key-value pairs
    tags HSTORE,
    
    -- Indexes
    CONSTRAINT unique_osm_id UNIQUE (osm_id)
);

-- Spatial index for fast location queries
CREATE INDEX idx_charging_stations_location ON charging_stations USING GIST (location);
CREATE INDEX idx_charging_stations_tags ON charging_stations USING GIN (tags);

-- Charging connectors table
CREATE TABLE charging_connectors (
    id BIGSERIAL PRIMARY KEY,
    station_id BIGINT REFERENCES charging_stations(id) ON DELETE CASCADE,
    
    -- Connector specifications
    connector_type VARCHAR(50) NOT NULL, -- 'ccs', 'chademo', 'type2', 'tesla'
    power_kw DECIMAL(5,2),
    voltage INT,
    amperage INT,
    current_type VARCHAR(20) CHECK (current_type IN ('AC', 'DC')),
    
    -- Real-time status
    status VARCHAR(20) DEFAULT 'unknown' CHECK (status IN ('available', 'occupied', 'faulty', 'unknown')),
    last_status_update TIMESTAMPTZ DEFAULT NOW(),
    
    -- Physical details
    count_available INT DEFAULT 1,
    count_total INT DEFAULT 1,
    
    -- Pricing
    price_per_kwh DECIMAL(8,4),
    price_per_minute DECIMAL(8,4),
    session_fee DECIMAL(8,2),
    
    -- Indexes
    CONSTRAINT fk_station FOREIGN KEY (station_id) REFERENCES charging_stations(id)
);

CREATE INDEX idx_connectors_station ON charging_connectors(station_id);
CREATE INDEX idx_connectors_status ON charging_connectors(status);

-- Amenities table (linked to OSM data)
CREATE TABLE station_amenities (
    id BIGSERIAL PRIMARY KEY,
    station_id BIGINT REFERENCES charging_stations(id) ON DELETE CASCADE,
    amenity_type VARCHAR(100) NOT NULL, -- 'restaurant', 'cafe', 'parking', 'toilets'
    name VARCHAR(255),
    distance_meters INT,
    
    -- Index
    CONSTRAINT fk_station_amenity FOREIGN KEY (station_id) REFERENCES charging_stations(id)
);

CREATE INDEX idx_amenities_station ON station_amenities(station_id);













-- User sessions and real-time data
CREATE TABLE charging_sessions (
    id BIGSERIAL PRIMARY KEY,
    station_id BIGINT REFERENCES charging_stations(id),
    connector_id BIGINT REFERENCES charging_connectors(id),
    user_id BIGINT, -- Reference to your users table
    
    start_time TIMESTAMPTZ DEFAULT NOW(),
    end_time TIMESTAMPTZ,
    energy_delivered_kwh DECIMAL(8,2),
    total_cost DECIMAL(8,2),
    
    status VARCHAR(20) DEFAULT 'active'
);

-- Historical availability patterns
CREATE TABLE availability_patterns (
    id BIGSERIAL PRIMARY KEY,
    station_id BIGINT REFERENCES charging_stations(id),
    
    -- Time patterns
    day_of_week INT, -- 0-6 (Sunday-Saturday)
    hour_of_day INT, -- 0-23
    
    -- Statistics
    avg_availability_rate DECIMAL(5,4), -- 0.0 to 1.0
    typical_wait_time_minutes INT,
    sample_size INT,
    
    -- Index
    UNIQUE(station_id, day_of_week, hour_of_day)
);