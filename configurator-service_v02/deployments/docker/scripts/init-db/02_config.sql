INSERT INTO connector_types (name, description) VALUES
    ('Type 1 (J1772)', 'Standard North American connector for AC charging'),
    ('Type 2 (Mennekes)', 'European standard for AC charging'),
    ('CCS1', 'Combined Charging System Type 1 for DC fast charging'),
    ('CCS2', 'Combined Charging System Type 2 for DC fast charging'),
    ('CHAdeMO', 'Japanese DC fast charging standard'),
    ('Tesla Supercharger', 'Tesla proprietary DC fast charging'),
    ('GB/T', 'Chinese national standard for AC and DC charging'),
    ('Tesla Destination', 'Tesla proprietary AC charging')
ON CONFLICT (name) DO NOTHING;

INSERT INTO connector_status (name, description) VALUES
    ('available', 'Charging station is available for use'),
    ('occupied', 'Charging station is currently in use'),
    ('faulty', 'Charging station is faulty and not operational'),
    ('unknown', 'Status of charging station is unknown'),
    ('reserved', 'Charging station is reserved')
ON CONFLICT (name) DO NOTHING;