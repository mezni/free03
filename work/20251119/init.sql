-- ===================================
-- 1. Networks (Aggregate Root)
-- ===================================
CREATE TABLE networks (
    id              UUID PRIMARY KEY,
    name            TEXT NOT NULL,

    network_type    TEXT NOT NULL CHECK (network_type IN ('INDIVIDUAL', 'COMPANY')),

    support_phone   TEXT,
    support_email   TEXT,

    is_live         BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified     BOOLEAN NOT NULL DEFAULT FALSE,
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,

    created_by      UUID NOT NULL,
    updated_by      UUID,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ===================================
-- 2. Persons (UPDATED)
-- ===================================
CREATE TABLE persons (
    id              UUID PRIMARY KEY,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    email           TEXT,
    phone           TEXT,

    job_title       TEXT,
    department      TEXT,

    role_type       VARCHAR(50) NOT NULL CHECK (
                        role_type IN ('ADMIN', 'BILLING', 'TECHNICAL', 'OPERATIONS', 'GENERAL')
                    ),

    is_live         BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified     BOOLEAN NOT NULL DEFAULT FALSE,   -- NEW
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,    -- NEW

    created_by      UUID NOT NULL,
    updated_by      UUID,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

-- ===================================
-- 3. Individual Network (1:1 Person)
-- ===================================
CREATE TABLE network_individuals (
    network_id  UUID PRIMARY KEY REFERENCES networks(id) ON DELETE CASCADE,
    person_id   UUID NOT NULL REFERENCES persons(id) ON DELETE RESTRICT
);

ALTER TABLE network_individuals
ADD CONSTRAINT check_network_is_individual
CHECK ((SELECT network_type FROM networks WHERE id = network_id) = 'INDIVIDUAL');

-- ===================================
-- 4. Company Network
-- ===================================
CREATE TABLE companies (
    network_id          UUID PRIMARY KEY REFERENCES networks(id) ON DELETE CASCADE,
    legal_name          TEXT NOT NULL,
    registration_number TEXT NOT NULL,
    website             TEXT,

    company_type        TEXT NOT NULL CHECK (
                            company_type IN ('COMPANY', 'COOPERATIVE', 'GOVERNMENT')
                         ),

    company_size        TEXT,

    is_live             BOOLEAN NOT NULL DEFAULT TRUE,

    created_by          UUID NOT NULL,
    updated_by          UUID,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE companies
ADD CONSTRAINT check_network_is_company
CHECK ((SELECT network_type FROM networks WHERE id = network_id) = 'COMPANY');

-- ===================================
-- 5. Company People (1..N)
-- ===================================
CREATE TABLE company_people (
    company_id  UUID NOT NULL REFERENCES companies(network_id) ON DELETE CASCADE,
    person_id   UUID NOT NULL REFERENCES persons(id) ON DELETE RESTRICT,
    PRIMARY KEY (company_id, person_id)
);
