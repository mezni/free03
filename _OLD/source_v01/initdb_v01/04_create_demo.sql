INSERT INTO users (username, email, password, role) VALUES
('admin', 'admin@example.com', 'password123', 'admin'),
('moderator', 'moderator@example.com', 'password123', 'moderator'),
('user', 'user@example.com', 'password123', 'user');

INSERT INTO charging_stations (osm_id, name, address, location, created_by)
VALUES
(1020250001,'STEG Charging Station - Lac', 'Lac de Tunis, near Tunis City Center', ST_Point(10.2417, 36.8380, 4326), current_user_id()),
(1020250002,'Hotel Golden Tulip El Mechtel', 'Avenue Ouled Haffouz, Tunis', ST_Point(10.2087, 36.8374, 4326), current_user_id()),
(1020250003,'Tunisia Mall Charging Point', 'Les Berges du Lac, Tunis', ST_Point(10.2376, 36.8510, 4326), current_user_id()),
(1020250004,'Energym Charging Station', 'La Goulette, Tunis', ST_Point(10.3135, 36.8185, 4326), current_user_id()),
(1020250005,'The Residence Tunis', 'Gammarth, Tunis', ST_Point(10.3234, 36.9542, 4326), current_user_id()),
(1020250006,'Carrefour Charging Point', 'Marsa, Tunis', ST_Point(10.3247, 36.8782, 4326), current_user_id());