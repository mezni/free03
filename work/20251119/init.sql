-- ===================================
-- 1. NETWORKS (Aggregate Root)
-- ===================================
CREATE TABLE networks (
    network_id        UUID PRIMARY KEY,
    name              VARCHAR(255),  -- for companies
    network_type      VARCHAR(20) NOT NULL CHECK (network_type IN ('INDIVIDUAL', 'COMPANY')),
    support_phone     VARCHAR(50),
    support_email     VARCHAR(255),

    is_verified       BOOLEAN DEFAULT FALSE,
    is_active         BOOLEAN DEFAULT TRUE,
    is_live           BOOLEAN DEFAULT TRUE,

    created_by        UUID NOT NULL,
    updated_by        UUID,
    created_at        TIMESTAMP DEFAULT NOW(),
    updated_at        TIMESTAMP
);

-- ===================================
-- 2. INDIVIDUAL NETWORK (1 network = 1 individual)
-- ===================================
CREATE TABLE individuals (
    individual_id     UUID PRIMARY KEY,
    network_id        UUID NOT NULL UNIQUE REFERENCES networks(network_id) ON DELETE CASCADE
);

-- ===================================
-- 3. COMPANY NETWORK (1 network = 1 company)
-- ===================================
CREATE TABLE companies (
    company_id        UUID PRIMARY KEY,
    network_id        UUID NOT NULL UNIQUE REFERENCES networks(network_id) ON DELETE CASCADE,

    website           VARCHAR(255),
    company_type      VARCHAR(50) CHECK (company_type IN ('COMPANY', 'COOPERATIVE', 'GOVERNMENT')),
    company_size      VARCHAR(50)
);

-- ===================================
-- 4. PERSONS
-- ===================================
CREATE TABLE persons (
    person_id     UUID PRIMARY KEY,

    individual_id UUID REFERENCES individuals(individual_id) ON DELETE CASCADE,
    company_id    UUID REFERENCES companies(company_id) ON DELETE CASCADE,

    full_name     VARCHAR(255) NOT NULL,
    email         VARCHAR(255) UNIQUE,
    phone         VARCHAR(50),

    job_title     VARCHAR(255),
    department    VARCHAR(255),
    role_type     VARCHAR(50) NOT NULL CHECK (
                        role_type IN ('ADMIN', 'BILLING', 'TECHNICAL', 'OPERATIONS', 'GENERAL')
                    ),

    is_verified   BOOLEAN DEFAULT FALSE,
    is_active     BOOLEAN DEFAULT TRUE,
    is_live       BOOLEAN DEFAULT TRUE,

    created_by    UUID NOT NULL,
    updated_by    UUID,
    created_at    TIMESTAMP DEFAULT NOW(),
    updated_at    TIMESTAMP
);

-- ===================================
-- 5. STATIONS
-- ===================================
CREATE TABLE stations (
    station_id          UUID PRIMARY KEY,
    network_id          UUID NOT NULL REFERENCES networks(network_id) ON DELETE CASCADE,

    name                VARCHAR(255) NOT NULL,
    location            JSONB,                  -- optional {lat, lng, address}
    tags                JSONB,                  -- e.g., ["fast-charging", "covered"]

    operational_status  VARCHAR(50) NOT NULL CHECK (
                            operational_status IN ('ACTIVE', 'MAINTENANCE', 'OUT_OF_SERVICE', 'COMMISSIONING')
                        ),
    verification_status VARCHAR(50) NOT NULL DEFAULT 'PENDING' CHECK (
                            verification_status IN ('PENDING', 'VERIFIED', 'REJECTED')
                        ),

    is_live             BOOLEAN DEFAULT TRUE,
    created_by          UUID NOT NULL,
    updated_by          UUID,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP
);

-- ===================================
-- 6. CONNECTOR TYPES
-- ===================================
CREATE TABLE connector_types (
    connector_type_id   UUID PRIMARY KEY,
    name                VARCHAR(50) NOT NULL UNIQUE,  -- e.g., 'TYPE2', 'CCS', 'CHADEMO'
    description         TEXT,

    is_live             BOOLEAN DEFAULT TRUE,
    is_active           BOOLEAN DEFAULT TRUE,
    is_verified         BOOLEAN DEFAULT FALSE,

    created_by          UUID NOT NULL,
    updated_by          UUID,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP
);

-- ===================================
-- 7. CONNECTORS (station can have 0..N connectors)
-- ===================================
CREATE TABLE connectors (
    connector_id        UUID PRIMARY KEY,
    station_id          UUID NOT NULL REFERENCES stations(station_id) ON DELETE CASCADE,
    connector_type_id   UUID NOT NULL REFERENCES connector_types(connector_type_id) ON DELETE RESTRICT,

    capacity_kw         NUMERIC(5,2),          -- e.g., 22.5 kW
    operational_status  VARCHAR(50) NOT NULL CHECK (
                            operational_status IN ('AVAILABLE', 'CHARGING', 'FAULTY', 'RESERVED', 'OFFLINE')
                        ),
    verification_status VARCHAR(50) NOT NULL DEFAULT 'PENDING' CHECK (
                            verification_status IN ('PENDING', 'VERIFIED', 'REJECTED')
                        ),
    
    tags                JSONB,                 -- optional labels

    is_live             BOOLEAN DEFAULT TRUE,
    is_active           BOOLEAN DEFAULT TRUE,
    is_verified         BOOLEAN DEFAULT FALSE,

    created_by          UUID NOT NULL,
    updated_by          UUID,
    created_at          TIMESTAMP DEFAULT NOW(),
    updated_at          TIMESTAMP
);
