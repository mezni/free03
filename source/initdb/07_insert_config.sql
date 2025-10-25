INSERT INTO access_types (name, description) VALUES
('public', 'Publicly accessible'),
('private', 'Private access only'),
('customers', 'Access restricted to customers');

INSERT INTO data_sources (name, description) VALUES
('osm', 'Data sourced from OpenStreetMap'),
('user_submitted', 'Data submitted by users'),
('commercial', 'Data from commercial providers');


INSERT INTO connector_types (name, description)
VALUES
('ccs', 'Combined Charging System'),
('chademo', 'CHAdeMO'),
('type2', 'Type 2 (Mennekes)'),
('tesla', 'Tesla Supercharger');

INSERT INTO current_types (name, description)
VALUES
('AC', 'Alternating Current'),
('DC', 'Direct Current');

INSERT INTO connector_statuses (name, description)
VALUES
('available', 'Charging station is available for use'),
('occupied', 'Charging station is currently in use'),
('faulty', 'Charging station is faulty and not operational'),
('unknown', 'Status of charging station is unknown');