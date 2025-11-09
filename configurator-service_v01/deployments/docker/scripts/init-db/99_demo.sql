INSERT INTO stations (
    osm_id,
    name,
    address,
    location,
    operator,
    tags,
    created_by
)
VALUES
(
    202500000001,
    'STEG Charging Station - Lac',
    'Lac de Tunis, near Tunis City Center',
    ST_GeogFromText('SRID=4326;POINT(10.2417 36.8380)'),
    'STEG',
    hstore(ARRAY[
        'amenity', 'charging_station',
        'capacity', '4',
        'fee', 'no',
        'parking_fee', 'no',
        'access', 'public'
    ]),
    'f47ac10b-58cc-4372-a567-0e02b2c3d479'
),
(
    202500000002,
    'Hotel Golden Tulip El Mechtel',
    'Avenue Ouled Haffouz, Tunis',
    ST_GeogFromText('SRID=4326;POINT(10.2087 36.8374)'),
    'Golden Tulip',
    hstore(ARRAY[
        'amenity', 'charging_station',
        'capacity', '2',
        'fee', 'yes',
        'parking_fee', 'yes',
        'access', 'customers'
    ]),
    'f47ac10b-58cc-4372-a567-0e02b2c3d479'
),
(
    202500000003,
    'Tunisia Mall Charging Point',
    'Les Berges du Lac, Tunis',
    ST_GeogFromText('SRID=4326;POINT(10.2376 36.8510)'),
    'Tunisia Mall',
    hstore(ARRAY[
        'amenity', 'charging_station',
        'capacity', '6',
        'fee', 'no',
        'parking_fee', 'yes',
        'access', 'public'
    ]),
    'f47ac10b-58cc-4372-a567-0e02b2c3d479'
),
(
    202500000004,
    'Energym Charging Station',
    'La Goulette, Tunis',
    ST_GeogFromText('SRID=4326;POINT(10.3050 36.8185)'),
    'Energym',
    hstore(ARRAY[
        'amenity', 'charging_station',
        'capacity', '8',
        'fee', 'yes',
        'parking_fee', 'no',
        'access', 'public'
    ]),
    'f47ac10b-58cc-4372-a567-0e02b2c3d479'
),
(
    202500000005,
    'The Residence Tunis',
    'Gammarth, Tunis',
    ST_GeogFromText('SRID=4326;POINT(10.3234 36.9542)'),
    'The Residence',
    hstore(ARRAY[
        'amenity', 'charging_station',
        'capacity', '2',
        'fee', 'no',
        'parking_fee', 'no',
        'access', 'customers'
    ]),
    'f47ac10b-58cc-4372-a567-0e02b2c3d479'
),
(
    202500000006,
    'Carrefour Charging Point',
    'Marsa, Tunis',
    ST_GeogFromText('SRID=4326;POINT(10.3247 36.8782)'),
    'Carrefour',
    hstore(ARRAY[
        'amenity', 'charging_station',
        'capacity', '4',
        'fee', 'no',
        'parking_fee', 'no',
        'access', 'public'
    ]),
    'f47ac10b-58cc-4372-a567-0e02b2c3d479'
),
(
    202500000007,
    'Aeroport Tunis-Carthage',
    'Aéroport International de Tunis-Carthage',
    ST_GeogFromText('SRID=4326;POINT(10.2272 36.8510)'),
    'Tunis Air',
    hstore(ARRAY[
        'amenity', 'charging_station',
        'capacity', '4',
        'fee', 'yes',
        'parking_fee', 'yes',
        'access', 'public'
    ]),
    'f47ac10b-58cc-4372-a567-0e02b2c3d479'
),
(
    202500000008,
    'Station ENNOUR',
    'Route de La Marsa, Carthage',
    ST_GeogFromText('SRID=4326;POINT(10.3215 36.8612)'),
    'ENNOUR',
    hstore(ARRAY[
        'amenity', 'charging_station',
        'capacity', '2',
        'fee', 'yes',
        'parking_fee', 'no',
        'access', 'public'
    ]),
    'f47ac10b-58cc-4372-a567-0e02b2c3d479'
);