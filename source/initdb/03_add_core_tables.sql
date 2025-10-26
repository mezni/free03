CREATE TABLE charging_stations (
    id BIGSERIAL PRIMARY KEY,
    osm_id BIGINT UNIQUE NOT NULL, 
    name VARCHAR(255) NOT NULL,
    address TEXT,
    
    location GEOGRAPHY(Point, 4326) NOT NULL,

    tags HSTORE,
        
    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMPTZ,

    
    CONSTRAINT fk_charging_stations_created_by FOREIGN KEY (created_by) REFERENCES users(id),
    CONSTRAINT fk_charging_stations_updated_by FOREIGN KEY (updated_by) REFERENCES users(id)
);

CREATE TABLE station_connectors (
    id BIGSERIAL PRIMARY KEY,
    station_id BIGINT NOT NULL,
    connector_type_id BIGINT NOT NULL,
    status_id BIGINT NOT NULL,
    current_type_id BIGINT NOT NULL,    
    power_kw DECIMAL(5,2),
    voltage INT,
    amperage INT,
    count_available INT DEFAULT 1 CHECK (count_available >= 0),
    count_total INT DEFAULT 1 CHECK (count_total >= 1 AND count_total >= count_available),

    created_by INTEGER NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMPTZ,

    CONSTRAINT fk_station_connectors_station FOREIGN KEY (station_id) REFERENCES charging_stations(id) ON DELETE CASCADE,
    CONSTRAINT fk_station_connectors_connector_type FOREIGN KEY (connector_type_id) REFERENCES connector_types(id) ON DELETE CASCADE,
    CONSTRAINT fk_station_connectors_status FOREIGN KEY (status_id) REFERENCES  connector_statuses(id) ON DELETE CASCADE,
    CONSTRAINT fk_station_connectors_current_type FOREIGN KEY (current_type_id) REFERENCES current_types(id) ON DELETE CASCADE,
    CONSTRAINT fk_station_connectors_created_by FOREIGN KEY (created_by) REFERENCES users(id),
    CONSTRAINT fk_station_connectors_updated_by FOREIGN KEY (updated_by) REFERENCES users(id),
    CONSTRAINT unique_station_connector UNIQUE (station_id, connector_type_id, current_type_id)
);