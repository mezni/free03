-- Create networks table with TEXT and check constraint
CREATE TABLE networks (
    network_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(20) NOT NULL CHECK (type IN ('individual', 'company')),
    contact_email VARCHAR(255),
    phone_number VARCHAR(50),
    address TEXT,
    created_by UUID NOT NULL,
    updated_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create companies table
CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    network_id INTEGER UNIQUE NOT NULL,
    business_registration_number VARCHAR(100),
    website_url VARCHAR(255),
    created_by UUID NOT NULL,
    updated_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (network_id) REFERENCES networks(network_id) ON DELETE CASCADE
);


CREATE TABLE stations (
    station_id SERIAL PRIMARY KEY,
    network_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    location GEOGRAPHY(Point, 4326) NOT NULL,
    tags HSTORE,
    osm_id BIGINT,
    is_operational BOOLEAN DEFAULT TRUE,
    created_by UUID NOT NULL,
    updated_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (network_id) REFERENCES networks(network_id) ON DELETE CASCADE
);

-- Create index for spatial queries
CREATE INDEX idx_stations_location ON stations USING GIST (location);
CREATE INDEX idx_stations_network_id ON stations (network_id);
CREATE INDEX idx_stations_operational ON stations (is_operational);

-----------------------------------------------------




-- First, make sure you have a network (if you don't have one already)
INSERT INTO networks (name, type, created_by) 
VALUES ('California EV Network', 'company', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11')
RETURNING network_id;

-- Then insert stations (replace 1 with the actual network_id from above)
INSERT INTO stations (
    network_id, 
    name, 
    address, 
    city, 
    state, 
    country, 
    postal_code, 
    location, 
    tags, 
    osm_id, 
    is_operational, 
    created_by
) VALUES 
(
    1,  -- network_id
    'Downtown Charging Station',
    '123 Main Street',
    'San Francisco',
    'California', 
    'United States',
    '94105',
    ST_GeogFromText('POINT(-122.399677 37.787994)'),
    '"amenity"=>"charging_station", "capacity"=>"4", "operator"=>"EVGo", "socket"=>"type2"',
    123456789,
    TRUE,
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
),
(
    1,
    'Shopping Mall Charging Hub', 
    '456 Market Street',
    'San Francisco',
    'California',
    'United States', 
    '94102',
    ST_GeogFromText('POINT(-122.407235 37.784140)'),
    '"amenity"=>"charging_station", "capacity"=>"8", "access"=>"public", "socket"=>"ccs"',
    987654321,
    TRUE,
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
),
(
    1,
    'Airport Fast Charger',
    '789 Airport Boulevard', 
    'San Francisco',
    'California',
    'United States',
    '94128',
    ST_GeogFromText('POINT(-122.374447 37.615223)'),
    '"amenity"=>"charging_station", "capacity"=>"6", "operator"=>"Tesla", "fast_charging"=>"true"',
    555555555,
    TRUE, 
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
);






CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_network_updated_at
BEFORE UPDATE ON networks
FOR EACH ROW
EXECUTE PROCEDURE update_updated_at();


1. Networks Table
sql

CREATE TABLE networks (
    network_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type ENUM('individual', 'company') NOT NULL,
    contact_email VARCHAR(255),
    phone_number VARCHAR(50),
    address TEXT,
    created_by UUID NOT NULL, -- Reference to external user ID
    updated_by UUID, -- Reference to external user ID
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

2. Companies Table
sql

CREATE TABLE companies (
    company_id SERIAL PRIMARY KEY,
    network_id INTEGER UNIQUE NOT NULL,
    business_registration_number VARCHAR(100),
    website_url VARCHAR(255),
    created_by UUID NOT NULL,
    updated_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (network_id) REFERENCES networks(network_id) ON DELETE CASCADE
);

3. Connector Types Table
sql

CREATE TABLE connector_types (
    connector_type_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    standard VARCHAR(100),
    current_type ENUM('AC', 'DC') NOT NULL,
    typical_power_kw DECIMAL(6, 2),
    pin_configuration VARCHAR(100),
    is_public_standard BOOLEAN DEFAULT TRUE,
    created_by UUID NOT NULL,
    updated_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

4. Stations Table
sql

CREATE TABLE stations (
    station_id SERIAL PRIMARY KEY,
    network_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    location GEOGRAPHY(Point, 4326) NOT NULL,
    tags HSTORE,
    osm_id BIGINT,
    is_operational BOOLEAN DEFAULT TRUE,
    created_by UUID NOT NULL,
    updated_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (network_id) REFERENCES networks(network_id) ON DELETE CASCADE
);

5. Connectors Table
sql

CREATE TABLE connectors (
    connector_id SERIAL PRIMARY KEY,
    station_id INTEGER NOT NULL,
    connector_type_id INTEGER NOT NULL,
    power_level_kw DECIMAL(6, 2) NOT NULL,
    status ENUM('available', 'occupied', 'out_of_service', 'reserved') DEFAULT 'available',
    max_voltage INTEGER,
    max_amperage INTEGER,
    serial_number VARCHAR(100),
    manufacturer VARCHAR(100),
    model VARCHAR(100),
    installation_date DATE,
    last_maintenance_date DATE,
    created_by UUID NOT NULL,
    updated_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(station_id) ON DELETE CASCADE,
    FOREIGN KEY (connector_type_id) REFERENCES connector_types(connector_type_id)
);

6. Charging Sessions Table
sql

CREATE TABLE charging_sessions (
    session_id SERIAL PRIMARY KEY,
    connector_id INTEGER NOT NULL,
    user_id UUID NOT NULL, -- External user who is charging their vehicle
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    energy_delivered_kwh DECIMAL(8, 2),
    total_cost DECIMAL(8, 2),
    payment_status ENUM('pending', 'paid', 'failed', 'refunded') DEFAULT 'pending',
    payment_method VARCHAR(50),
    session_status ENUM('active', 'completed', 'cancelled', 'interrupted') DEFAULT 'active',
    initiated_by UUID NOT NULL, -- User who started the session
    ended_by UUID, -- User who ended the session
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (connector_id) REFERENCES connectors(connector_id)
);

7. Station Availability Table
sql

CREATE TABLE station_availability (
    availability_id SERIAL PRIMARY KEY,
    station_id INTEGER NOT NULL,
    day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6),
    open_time TIME,
    close_time TIME,
    is_24_hours BOOLEAN DEFAULT FALSE,
    created_by UUID NOT NULL,
    updated_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (station_id) REFERENCES stations(station_id) ON DELETE CASCADE
);

8. Pricing Table
sql

CREATE TABLE pricing (
    pricing_id SERIAL PRIMARY KEY,
    network_id INTEGER NOT NULL,
    connector_type_id INTEGER,
    pricing_model ENUM('per_kwh', 'per_minute', 'flat_rate', 'membership') NOT NULL,
    cost_per_kwh DECIMAL(8, 4),
    cost_per_minute DECIMAL(8, 4),
    flat_rate_cost DECIMAL(8, 2),
    membership_fee DECIMAL(8, 2),
    start_time TIME,
    end_time TIME,
    day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6),
    is_active BOOLEAN DEFAULT TRUE,
    effective_from DATE NOT NULL,
    effective_until DATE,
    created_by UUID NOT NULL,
    updated_by UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (network_id) REFERENCES networks(network_id),
    FOREIGN KEY (connector_type_id) REFERENCES connector_types(connector_type_id)
);

9. API Audit Log Table (Additional - For tracking API calls)
sql

CREATE TABLE api_audit_log (
    audit_id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL, -- External user ID from auth server
    action VARCHAR(100) NOT NULL, -- e.g., 'create_station', 'start_charging'
    resource_type VARCHAR(50) NOT NULL, -- e.g., 'station', 'connector', 'session'
    resource_id INTEGER, -- ID of the affected resource
    ip_address INET,
    user_agent TEXT,
    request_method VARCHAR(10), -- GET, POST, PUT, DELETE
    status_code INTEGER,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

Complete Index Script
sql

-- Networks indexes
CREATE INDEX idx_networks_type ON networks(type);
CREATE INDEX idx_networks_name ON networks(name);
CREATE INDEX idx_networks_created_by ON networks(created_by);
CREATE INDEX idx_networks_updated_by ON networks(updated_by);

-- Stations indexes
CREATE INDEX idx_stations_location_geography ON stations USING GIST (location);
CREATE INDEX idx_stations_tags ON stations USING GIN (tags);
CREATE INDEX idx_stations_osm_id ON stations(osm_id);
CREATE INDEX idx_stations_network ON stations(network_id);
CREATE INDEX idx_stations_operational ON stations(is_operational);
CREATE INDEX idx_stations_city ON stations(city);
CREATE INDEX idx_stations_country ON stations(country);
CREATE INDEX idx_stations_created_by ON stations(created_by);
CREATE INDEX idx_stations_updated_by ON stations(updated_by);

-- Connector Types indexes
CREATE INDEX idx_connector_types_current ON connector_types(current_type);
CREATE INDEX idx_connector_types_standard ON connector_types(standard);
CREATE INDEX idx_connector_types_created_by ON connector_types(created_by);

-- Connectors indexes
CREATE INDEX idx_connectors_station ON connectors(station_id);
CREATE INDEX idx_connectors_type ON connectors(connector_type_id);
CREATE INDEX idx_connectors_status ON connectors(status);
CREATE INDEX idx_connectors_power ON connectors(power_level_kw);
CREATE INDEX idx_connectors_manufacturer ON connectors(manufacturer);
CREATE INDEX idx_connectors_created_by ON connectors(created_by);
CREATE INDEX idx_connectors_updated_by ON connectors(updated_by);

-- Charging Sessions indexes
CREATE INDEX idx_sessions_connector ON charging_sessions(connector_id);
CREATE INDEX idx_sessions_user ON charging_sessions(user_id);
CREATE INDEX idx_sessions_time ON charging_sessions(start_time, end_time);
CREATE INDEX idx_sessions_status ON charging_sessions(session_status);
CREATE INDEX idx_sessions_payment_status ON charging_sessions(payment_status);
CREATE INDEX idx_sessions_initiated_by ON charging_sessions(initiated_by);
CREATE INDEX idx_sessions_ended_by ON charging_sessions(ended_by);

-- Station Availability indexes
CREATE INDEX idx_availability_station ON station_availability(station_id);
CREATE INDEX idx_availability_day ON station_availability(day_of_week);
CREATE INDEX idx_availability_created_by ON station_availability(created_by);

-- Pricing indexes
CREATE INDEX idx_pricing_network ON pricing(network_id);
CREATE INDEX idx_pricing_connector_type ON pricing(connector_type_id);
CREATE INDEX idx_pricing_model ON pricing(pricing_model);
CREATE INDEX idx_pricing_active ON pricing(is_active);
CREATE INDEX idx_pricing_dates ON pricing(effective_from, effective_until);
CREATE INDEX idx_pricing_created_by ON pricing(created_by);

-- API Audit Log indexes
CREATE INDEX idx_audit_user ON api_audit_log(user_id);
CREATE INDEX idx_audit_action ON api_audit_log(action);
CREATE INDEX idx_audit_resource ON api_audit_log(resource_type, resource_id);
CREATE INDEX idx_audit_created_at ON api_audit_log(created_at);
CREATE INDEX idx_audit_ip ON api_audit_log(ip_address);

Example Usage in API

Your API would receive the user ID from the authentication server and use it in all operations:
sql

-- Creating a new station
INSERT INTO stations (
    network_id, name, address, city, location, tags, osm_id, created_by
) VALUES (
    1, 'New Charging Station', '456 Oak St', 'Boston',
    ST_GeogFromText('POINT(-71.0589 42.3601)'),
    '"amenity"=>"charging_station"', 987654321,
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890' -- External user ID from JWT
);

-- Starting a charging session
INSERT INTO charging_sessions (
    connector_id, user_id, start_time, initiated_by
) VALUES (
    1, 
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890', -- User charging their vehicle
    CURRENT_TIMESTAMP,
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890' -- Same user initiated
);

-- Logging API call
INSERT INTO api_audit_log (
    user_id, action, resource_type, resource_id, ip_address, request_method, status_code
) VALUES (
    'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    'create_station',
    'station',
    1,
    '192.168.1.100',
    'POST',
    201
);





src/
├── lib.rs
├── main.rs
├── shared/
│   ├── mod.rs
│   ├── errors.rs
│   └── constants.rs
├── domain/
│   ├── mod.rs
│   ├── value_objects.rs
│   ├── repositories.rs
│   └── entities/
│       ├── mod.rs
│       ├── companies.rs
│       └── networks.rs
├── infrastructure/
│   ├── mod.rs
│   ├── config.rs          ← NEW FILE ADDED
│   ├── database.rs
│   ├── logger.rs
│   └── repositories/
│       ├── mod.rs
│       ├── companies.rs
│       └── networks.rs
├── application/
│   ├── mod.rs
│   ├── commands/
│   │   ├── mod.rs
│   │   ├── networks.rs
│   │   └── companies.rs
│   └── queries/
│       ├── mod.rs
│       ├── networks.rs
│       └── companies.rs
└── api/
    ├── mod.rs
    ├── dtos/
    │   ├── mod.rs
    │   ├── networks.rs
    │   └── companies.rs
    ├── handlers/
    │   ├── mod.rs
    │   ├── networks.rs
    │   └── companies.rs
    ├── openapi.rs
    └── routes.rs