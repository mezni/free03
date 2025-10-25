INSERT INTO access_types (name, description) VALUES
('public', 'Publicly accessible'),
('private', 'Private access only'),
('customers', 'Access restricted to customers');

INSERT INTO data_sources (name, description) VALUES
('osm', 'Data sourced from OpenStreetMap'),
('user_submitted', 'Data submitted by users'),
('commercial', 'Data from commercial providers');
