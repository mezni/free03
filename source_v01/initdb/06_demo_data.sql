-- Insert sample users
INSERT INTO users (username, email, password, role) VALUES
('admin', 'admin@charging.com', '$2b$12$LQv3c1yqBWVHxkd0L6k0uO9S6VY6Qk8JvY8cZc6vY6X2rV8c6vY6X', 'admin'),
('moderator', 'moderator@charging.com', '$2b$12$LQv3c1yqBWVHxkd0L6k0uO9S6VY6Qk8JvY8cZc6vY6X2rV8c6vY6X', 'moderator'),
('user1', 'user1@charging.com', '$2b$12$LQv3c1yqBWVHxkd0L6k0uO9S6VY6Qk8JvY8cZc6vY6X2rV8c6vY6X', 'user');


-- Insert sample charging stations (Tunis area) - FIXED hstore syntax
INSERT INTO charging_stations (osm_id, name, address, location, tags, created_by) VALUES
(202500000001, 'STEG Charging Station - Lac', 'Lac de Tunis, near Tunis City Center', 
 ST_GeogFromText('POINT(10.2417 36.8380)'),
 hstore(ARRAY[
    ['amenity', 'charging_station'],
    ['operator', 'STEG'],
    ['capacity', '4'],
    ['fee', 'no'],
    ['parking_fee', 'no'],
    ['access', 'public']
 ]), 1),

(202500000002, 'Hotel Golden Tulip El Mechtel', 'Avenue Ouled Haffouz, Tunis', 
 ST_GeogFromText('POINT(10.2087 36.8374)'),
 hstore(ARRAY[
    ['amenity', 'charging_station'],
    ['operator', 'Golden Tulip'],
    ['capacity', '2'],
    ['fee', 'yes'],
    ['parking_fee', 'yes'],
    ['access', 'customers']
 ]), 1),

(202500000003, 'Tunisia Mall Charging Point', 'Les Berges du Lac, Tunis', 
 ST_GeogFromText('POINT(10.2376 36.8510)'),
 hstore(ARRAY[
    ['amenity', 'charging_station'],
    ['operator', 'Tunisia Mall'],
    ['capacity', '6'],
    ['fee', 'no'],
    ['parking_fee', 'yes'],
    ['access', 'public']
 ]), 1),

(202500000004, 'Energym Charging Station', 'La Goulette, Tunis', 
 ST_GeogFromText('POINT(10.3050 36.8185)'),
 hstore(ARRAY[
    ['amenity', 'charging_station'],
    ['operator', 'Energym'],
    ['capacity', '8'],
    ['fee', 'yes'],
    ['parking_fee', 'no'],
    ['access', 'public']
 ]), 1),

(202500000005, 'The Residence Tunis', 'Gammarth, Tunis', 
 ST_GeogFromText('POINT(10.3234 36.9542)'),
 hstore(ARRAY[
    ['amenity', 'charging_station'],
    ['operator', 'The Residence'],
    ['capacity', '2'],
    ['fee', 'no'],
    ['parking_fee', 'no'],
    ['access', 'customers']
 ]), 1),

(202500000006, 'Carrefour Charging Point', 'Marsa, Tunis', 
 ST_GeogFromText('POINT(10.3247 36.8782)'),
 hstore(ARRAY[
    ['amenity', 'charging_station'],
    ['operator', 'Carrefour'],
    ['capacity', '4'],
    ['fee', 'no'],
    ['parking_fee', 'no'],
    ['access', 'public']
 ]), 1),

(202500000007, 'Aeroport Tunis-Carthage', 'Aéroport International de Tunis-Carthage', 
 ST_GeogFromText('POINT(10.2272 36.8510)'),
 hstore(ARRAY[
    ['amenity', 'charging_station'],
    ['operator', 'Tunis Air'],
    ['capacity', '4'],
    ['fee', 'yes'],
    ['parking_fee', 'yes'],
    ['access', 'public']
 ]), 1),

(202500000008, 'Station ENNOUR', 'Route de La Marsa, Carthage', 
 ST_GeogFromText('POINT(10.3215 36.8612)'),
 hstore(ARRAY[
    ['amenity', 'charging_station'],
    ['operator', 'ENNOUR'],
    ['capacity', '2'],
    ['fee', 'yes'],
    ['parking_fee', 'no'],
    ['access', 'public']
 ]), 1);

-- Insert sample connectors
INSERT INTO station_connectors (
    station_id, connector_type_id, status_id, current_type_id,
    power_kw, voltage, amperage, count_available, count_total, created_by
) VALUES 
-- STEG Station - Mixed connectors
(1, 1, 1, 1, 22.0, 400, 32, 2, 2, 1),  -- Type2 AC
(1, 2, 1, 2, 50.0, 500, 125, 1, 2, 1),  -- CCS DC

-- Golden Tulip - Fast charging
(2, 2, 1, 2, 150.0, 500, 300, 1, 1, 1), -- CCS DC
(2, 3, 2, 2, 50.0, 500, 125, 0, 1, 1),  -- CHAdeMO (occupied)

-- Tunisia Mall - Multiple types
(3, 1, 1, 1, 11.0, 230, 16, 3, 4, 1),   -- Type2 AC
(3, 2, 1, 2, 100.0, 500, 200, 1, 1, 1), -- CCS DC
(3, 3, 1, 2, 50.0, 500, 125, 1, 1, 1),  -- CHAdeMO

-- Energym - High power
(4, 2, 1, 2, 350.0, 1000, 350, 2, 2, 1), -- CCS DC Ultra Fast
(4, 4, 1, 2, 250.0, 480, 520, 2, 2, 1), -- Tesla Supercharger

-- The Residence - Standard
(5, 1, 1, 1, 22.0, 400, 32, 2, 2, 1),   -- Type2 AC

-- Carrefour - Mixed
(6, 1, 1, 1, 11.0, 230, 16, 2, 2, 1),   -- Type2 AC
(6, 5, 3, 1, 3.7, 230, 16, 0, 2, 1),    -- Schuko (faulty)

-- Airport - Fast charging
(7, 2, 1, 2, 150.0, 500, 300, 2, 2, 1), -- CCS DC
(7, 3, 1, 2, 50.0, 500, 125, 1, 2, 1),  -- CHAdeMO

-- ENNOUR - Standard
(8, 1, 1, 1, 22.0, 400, 32, 2, 2, 1);   -- Type2 AC