CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS hstore;

CREATE TABLE connector_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT
);


CREATE TABLE stations (
    id BIGSERIAL PRIMARY KEY,
    osm_id BIGINT UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    location GEOGRAPHY(Point, 4326) NOT NULL,
    operator VARCHAR(255) NOT NULL,
    tags HSTORE,
    created_by TEXT NOT NULL DEFAULT 'f47ac10b-58cc-4372-a567-0e02b2c3d479',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by TEXT,
    updated_at TIMESTAMPTZ
);
