CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'moderator', 'user')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

-- Insert some test data
INSERT INTO users (username, email, password, role) VALUES
('admin', 'admin@example.com', 'password123', 'admin'),
('moderator', 'moderator@example.com', 'password123', 'moderator'),
('user', 'user@example.com', 'password123', 'user');


CREATE TABLE charging_stations (
    id BIGSERIAL PRIMARY KEY,
    osm_id BIGINT UNIQUE NOT NULL, 
    name VARCHAR(255) NOT NULL,
    address TEXT,
    
    location GEOGRAPHY(Point, 4326) NOT NULL,
    
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMPTZ,
    
    -- Indexes
    CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES users(id),
    CONSTRAINT fk_updated_by FOREIGN KEY (updated_by) REFERENCES users(id)
);

CREATE INDEX idx_charging_stations_location ON charging_stations USING GIST (location);
CREATE INDEX idx_charging_stations_osm_id ON charging_stations (osm_id);


CREATE OR REPLACE FUNCTION current_user_id()
RETURNS INTEGER AS $$
DECLARE
    current_user_id INTEGER;
BEGIN
    current_user_id := 1;  
    RETURN current_user_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_charging_station_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_by := current_user_id();  
    NEW.updated_at := NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_charging_station_timestamp_trigger
BEFORE UPDATE ON charging_stations
FOR EACH ROW
EXECUTE PROCEDURE update_charging_station_timestamp();


INSERT INTO charging_stations (osm_id, name, address, location, created_by)
VALUES
(1020250001,'STEG Charging Station - Lac', 'Lac de Tunis, near Tunis City Center', ST_Point(10.2417, 36.8380, 4326), current_user_id()),
(1020250002,'Hotel Golden Tulip El Mechtel', 'Avenue Ouled Haffouz, Tunis', ST_Point(10.2087, 36.8374, 4326), current_user_id()),
(1020250003,'Tunisia Mall Charging Point', 'Les Berges du Lac, Tunis', ST_Point(10.2376, 36.8510, 4326), current_user_id()),
(1020250004,'Energym Charging Station', 'La Goulette, Tunis', ST_Point(10.3135, 36.8185, 4326), current_user_id()),
(1020250005,'The Residence Tunis', 'Gammarth, Tunis', ST_Point(10.3234, 36.9542, 4326), current_user_id()),
(1020250006,'Carrefour Charging Point', 'Marsa, Tunis', ST_Point(10.3247, 36.8782, 4326), current_user_id());