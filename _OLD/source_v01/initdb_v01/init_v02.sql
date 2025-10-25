chargingStations = [
            {
                name: "STEG Charging Station - Lac",
                coords: [36.8380, 10.2417],
                type: "Fast Charger",
                address: "Lac de Tunis, near Tunis City Center"
            },
            {
                name: "Hotel Golden Tulip El Mechtel",
                coords: [36.8374, 10.2087],
                type: "Type 2",
                address: "Avenue Ouled Haffouz, Tunis"
            },
            {
                name: "Tunisia Mall Charging Point",
                coords: [36.8510, 10.2376],
                type: "Type 2",
                address: "Les Berges du Lac, Tunis"
            },
            {
                name: "Energym Charging Station",
                coords: [36.8185, 10.3135],
                type: "Fast Charger",
                address: "La Goulette, Tunis"
            },
            {
                name: "The Residence Tunis",
                coords: [36.9542, 10.3234],
                type: "Type 2",
                address: "Gammarth, Tunis"
            },
            {
                name: "Carrefour Charging Point",
                coords: [36.8782, 10.3247],
                type: "Type 2",
                address: "Marsa, Tunis"
            }
        ];

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


CREATE TABLE charging_connectors (
    id BIGSERIAL PRIMARY KEY,
    station_id BIGINT NOT NULL,
    
    connector_type_id INTEGER NOT NULL REFERENCES connector_types(id),
    power_kw DECIMAL(5,2),
    voltage INT,
    amperage INT,
    current_type_id INTEGER NOT NULL REFERENCES current_types(id),
    
    status_id INTEGER NOT NULL REFERENCES connector_statuses(id),
    last_status_update TIMESTAMPTZ DEFAULT NOW(),
    
    count_available INT DEFAULT 1,
    count_total INT DEFAULT 1,
    
    price_per_kwh DECIMAL(8,4),
    price_per_minute DECIMAL(8,4),
    session_fee DECIMAL(8,2),
    
    -- Indexes
    CONSTRAINT fk_station FOREIGN KEY (station_id) REFERENCES charging_stations(id) ON DELETE CASCADE,
    CONSTRAINT fk_connector_type FOREIGN KEY (connector_type_id) REFERENCES connector_types(id),
    CONSTRAINT fk_current_type FOREIGN KEY (current_type_id) REFERENCES current_types(id),
    CONSTRAINT fk_status FOREIGN KEY (status_id) REFERENCES connector_statuses(id)
);

CREATE TABLE connector_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE current_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE connector_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    description TEXT
);

-- Insert initial data into connector_types, current_types, and connector_statuses tables
INSERT INTO connector_types (name, description) VALUES
('ccs', 'Combined Charging System'),
('chademo', 'CHAdeMO'),
('type2', 'Type 2'),
('tesla', 'Tesla Supercharger');

INSERT INTO current_types (name, description) VALUES
('AC', 'Alternating Current'),
('DC', 'Direct Current');

INSERT INTO connector_statuses (name, description) VALUES
('available', 'Connector is available'),
('occupied', 'Connector is occupied'),
('faulty', 'Connector is faulty'),
('unknown', 'Connector status is unknown');

-- Create indexes
CREATE INDEX idx_charging_connectors_station_id ON charging_connectors (station_id);


CREATE TABLE power_voltages (
    id SERIAL PRIMARY KEY,
    power_kw DECIMAL(5,2) NOT NULL,
    voltage INT NOT NULL,
    description TEXT,
    UNIQUE (power_kw, voltage)
);

-- Insert initial data into power_voltages table
INSERT INTO power_voltages (power_kw, voltage, description) VALUES
(3.7, 230, 'Single-phase AC, 3.7 kW, 230V'),
(7.4, 230, 'Single-phase AC, 7.4 kW, 230V'),
(11, 400, 'Three-phase AC, 11 kW, 400V'),
(22, 400, 'Three-phase AC, 22 kW, 400V'),
(50, 400, 'Three-phase AC, 50 kW, 400V'),
(100, 400, 'Three-phase AC, 100 kW, 400V'),
(150, 400, 'Three-phase AC, 150 kW, 400V'),
(250, 400, 'Three-phase AC, 250 kW, 400V'),
(350, 400, 'Three-phase AC, 350 kW, 400V');

-- Create index
CREATE INDEX idx_power_voltages_power_kw ON power_voltages (power_kw);
CREATE INDEX idx_power_voltages_voltage ON power_voltages (voltage);


CREATE TABLE powers (
    id SERIAL PRIMARY KEY,
    power_kw DECIMAL(5,2) NOT NULL,
    description TEXT,
    UNIQUE (power_kw)
);

CREATE TABLE voltages (
    id SERIAL PRIMARY KEY,
    voltage INT NOT NULL,
    description TEXT,
    UNIQUE (voltage)
);

CREATE TABLE amperages (
    id SERIAL PRIMARY KEY,
    amperage INT NOT NULL,
    description TEXT,
    UNIQUE (amperage)
);

-- Insert initial data into powers, voltages, and amperages tables
INSERT INTO powers (power_kw, description) VALUES
(3.7, '3.7 kW'),
(7.4, '7.4 kW'),
(11, '11 kW'),
(22, '22 kW'),
(50, '50 kW'),
(100, '100 kW'),
(150, '150 kW'),
(250, '250 kW'),
(350, '350 kW');

INSERT INTO voltages (voltage, description) VALUES
(230, '230V'),
(400, '400V'),
(480, '480V'),
(600, '600V');

INSERT INTO amperages (amperage, description) VALUES
(10, '10A'),
(16, '16A'),
(32, '32A'),
(63, '63A'),
(125, '125A');

-- Create indexes
CREATE INDEX idx_powers_power_kw ON powers (power_kw);
CREATE INDEX idx_voltages_voltage ON voltages (voltage);
CREATE INDEX idx_amperages_amperage ON amperages (amperage);