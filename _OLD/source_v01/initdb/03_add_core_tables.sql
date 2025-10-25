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

    tags HSTORE,
    
    -- Indexes
    CONSTRAINT fk_created_by FOREIGN KEY (created_by) REFERENCES users(id),
    CONSTRAINT fk_updated_by FOREIGN KEY (updated_by) REFERENCES users(id)
);

