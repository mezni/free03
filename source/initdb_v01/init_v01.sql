CREATE TABLE charging_stations (
    id BIGSERIAL PRIMARY KEY,
    osm_id BIGINT UNIQUE, 
    name VARCHAR(255) NOT NULL,
    operator VARCHAR(255),
    address TEXT,
    
    location GEOGRAPHY(Point, 4326),
    
    access_type_id INTEGER REFERENCES access_types(id),
    opening_hours TEXT,
    
    is_active BOOLEAN DEFAULT TRUE,
    last_updated TIMESTAMPTZ DEFAULT NOW(),
    data_source_id INTEGER REFERENCES data_sources(id),
    
    tags HSTORE,
    
    -- Indexes
    CONSTRAINT fk_access_type FOREIGN KEY (access_type_id) REFERENCES access_types(id),
    CONSTRAINT fk_data_source FOREIGN KEY (data_source_id) REFERENCES data_sources(id)
);

CREATE TABLE access_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE data_sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

-- Insert initial data into access_types and data_sources tables
INSERT INTO access_types (name, description) VALUES
('public', 'Publicly accessible'),
('private', 'Private access only'),
('customers', 'Access restricted to customers');

INSERT INTO data_sources (name, description) VALUES
('osm', 'Data sourced from OpenStreetMap'),
('user_submitted', 'Data submitted by users'),
('commercial', 'Data from commercial providers');

-- Create indexes
CREATE INDEX idx_charging_stations_location ON charging_stations USING GIST (location);
CREATE INDEX idx_charging_stations_osm_id ON charging_stations (osm_id);