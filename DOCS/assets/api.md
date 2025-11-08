
### ⚙️ Configurator-Service API Endpoints
| Category                  | Method   | Endpoint                                             | Description                            |
| ------------------------- | -------- | ---------------------------------------------------- | -------------------------------------- |
| **Charging Networks**     | `GET`    | `/api/v1/configurator/networks`                      | Get all charging networks              |
|                           | `GET`    | `/api/v1/configurator/networks/{id}`                 | Get a network by ID                    |
|                           | `POST`   | `/api/v1/configurator/networks`                      | Create a new network                   |
|                           | `PUT`    | `/api/v1/configurator/networks/{id}`                 | Update a network                       |
|                           | `DELETE` | `/api/v1/configurator/networks/{id}`                 | Delete a network                       |
| **Charging Operators**    | `GET`    | `/api/v1/configurator/operators`                     | List all operators                     |
|                           | `GET`    | `/api/v1/configurator/operators/{id}`                | Get operator details                   |
|                           | `POST`   | `/api/v1/configurator/operators`                     | Create a new operator                  |
|                           | `PUT`    | `/api/v1/configurator/operators/{id}`                | Update operator info                   |
|                           | `DELETE` | `/api/v1/configurator/operators/{id}`                | Delete operator                        |
| **Charging Stations**     | `GET`    | `/api/v1/configurator/stations`                      | List all stations                      |
|                           | `GET`    | `/api/v1/configurator/stations/{id}`                 | Get station details by ID              |
|                           | `GET`    | `/api/v1/configurator/stations/network/{network_id}` | List stations for a network            |
|                           | `POST`   | `/api/v1/configurator/stations`                      | Create a new charging station          |
|                           | `PUT`    | `/api/v1/configurator/stations/{id}`                 | Update charging station                |
|                           | `DELETE` | `/api/v1/configurator/stations/{id}`                 | Delete a station                       |
| **Charging Connectors**   | `GET`    | `/api/v1/configurator/connectors`                    | List all connectors                    |
|                           | `GET`    | `/api/v1/configurator/connectors/{id}`               | Get connector details                  |
|                           | `POST`   | `/api/v1/configurator/connectors`                    | Create a new connector                 |
|                           | `PUT`    | `/api/v1/configurator/connectors/{id}`               | Update connector details               |
|                           | `DELETE` | `/api/v1/configurator/connectors/{id}`               | Delete connector                       |
| **Connector Types**       | `GET`    | `/api/v1/configurator/connector-types`               | List all connector types               |
|                           | `POST`   | `/api/v1/configurator/connector-types`               | Add a new connector type               |
|                           | `PUT`    | `/api/v1/configurator/connector-types/{id}`          | Update a connector type                |
|                           | `DELETE` | `/api/v1/configurator/connector-types/{id}`          | Delete a connector type                |
| **Availability**          | `GET`    | `/api/v1/configurator/availability`                  | List all availability statuses         |
|                           | `POST`   | `/api/v1/configurator/availability`                  | Add new availability status            |
|                           | `PUT`    | `/api/v1/configurator/availability/{id}`             | Update availability status             |
|                           | `DELETE` | `/api/v1/configurator/availability/{id}`             | Delete availability status             |
| **Station Status**        | `GET`    | `/api/v1/configurator/station-status`                | List all station statuses              |
|                           | `POST`   | `/api/v1/configurator/station-status`                | Create new station status              |
|                           | `PUT`    | `/api/v1/configurator/station-status/{id}`           | Update station status                  |
|                           | `DELETE` | `/api/v1/configurator/station-status/{id}`           | Delete station status                  |
| **Owner Types**           | `GET`    | `/api/v1/configurator/owner-types`                   | List owner types (company, individual) |
|                           | `POST`   | `/api/v1/configurator/owner-types`                   | Add a new owner type                   |
|                           | `PUT`    | `/api/v1/configurator/owner-types/{id}`              | Update owner type                      |
|                           | `DELETE` | `/api/v1/configurator/owner-types/{id}`              | Delete owner type                      |
| **Roles**                 | `GET`    | `/api/v1/configurator/roles`                         | List available operator roles          |
|                           | `POST`   | `/api/v1/configurator/roles`                         | Add a new operator role                |
|                           | `PUT`    | `/api/v1/configurator/roles/{id}`                    | Update role                            |
|                           | `DELETE` | `/api/v1/configurator/roles/{id}`                    | Delete role                            |
| **Metadata & Versioning** | `GET`    | `/api/v1/configurator/version`                       | Get service version info               |
|                           | `GET`    | `/api/v1/configurator/health`                        | Health check endpoint                  |




-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS hstore;

------------------------------------------------------------
-- USERS (federated from auth-service, mirrored by ID only)
------------------------------------------------------------
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(255),
    full_name VARCHAR(255),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

------------------------------------------------------------
-- OWNER TYPES (Company, Individual)
------------------------------------------------------------
CREATE TABLE owner_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

------------------------------------------------------------
-- CHARGING NETWORKS (a network of stations, e.g., Tesla, ChargePoint)
------------------------------------------------------------
CREATE TABLE charging_networks (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    owner_type_id INT REFERENCES owner_types(id) ON DELETE SET NULL,
    description TEXT,
    contact_email VARCHAR(255),
    contact_phone VARCHAR(50),
    website VARCHAR(255),
    created_by BIGINT REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by BIGINT REFERENCES users(id),
    updated_at TIMESTAMPTZ
);

------------------------------------------------------------
-- CHARGING OPERATORS (manage stations — either individuals or companies)
------------------------------------------------------------
CREATE TABLE charging_operators (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES users(id) ON DELETE CASCADE,
    network_id BIGINT REFERENCES charging_networks(id) ON DELETE CASCADE,
    role_id INT,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

------------------------------------------------------------
-- OPERATOR ROLES (Manager, Technician, Viewer, etc.)
------------------------------------------------------------
CREATE TABLE operator_roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

ALTER TABLE charging_operators
    ADD CONSTRAINT fk_operator_role FOREIGN KEY (role_id)
    REFERENCES operator_roles(id) ON DELETE SET NULL;

------------------------------------------------------------
-- CHARGING STATION STATUS (Active, Inactive, Maintenance)
------------------------------------------------------------
CREATE TABLE station_status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

------------------------------------------------------------
-- CHARGING STATIONS
------------------------------------------------------------
CREATE TABLE charging_stations (
    id BIGSERIAL PRIMARY KEY,
    osm_id BIGINT UNIQUE,
    network_id BIGINT REFERENCES charging_networks(id) ON DELETE CASCADE,
    operator_id BIGINT REFERENCES charging_operators(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    address TEXT,
    location GEOGRAPHY(Point, 4326) NOT NULL,
    tags HSTORE,
    status_id INT REFERENCES station_status(id) ON DELETE SET NULL,
    created_by BIGINT REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_by BIGINT REFERENCES users(id),
    updated_at TIMESTAMPTZ
);

------------------------------------------------------------
-- CONNECTOR TYPES (CCS, CHAdeMO, Type2, etc.)
------------------------------------------------------------
CREATE TABLE connector_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    power_kw NUMERIC(10,2),
    voltage NUMERIC(10,2),
    current NUMERIC(10,2)
);

------------------------------------------------------------
-- CONNECTOR AVAILABILITY (Available, Occupied, OutOfOrder)
------------------------------------------------------------
CREATE TABLE connector_availability (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT
);

------------------------------------------------------------
-- CHARGING CONNECTORS
------------------------------------------------------------
CREATE TABLE charging_connectors (
    id BIGSERIAL PRIMARY KEY,
    station_id BIGINT REFERENCES charging_stations(id) ON DELETE CASCADE,
    connector_type_id INT REFERENCES connector_types(id) ON DELETE SET NULL,
    availability_id INT REFERENCES connector_availability(id) ON DELETE SET NULL,
    power_output_kw NUMERIC(10,2),
    socket_count INT DEFAULT 1,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ
);

------------------------------------------------------------
-- AUDIT LOG (optional)
------------------------------------------------------------
CREATE TABLE audit_logs (
    id BIGSERIAL PRIMARY KEY,
    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT NOT NULL,
    action VARCHAR(50) NOT NULL, -- e.g., CREATE, UPDATE, DELETE
    performed_by BIGINT REFERENCES users(id),
    performed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    details JSONB
);
