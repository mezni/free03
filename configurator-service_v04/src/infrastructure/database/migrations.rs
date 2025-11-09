use sqlx::{Executor, PgPool};

pub async fn run_migrations(pool: &PgPool) -> Result<(), sqlx::Error> {
    // Enable PostGIS extension
    pool.execute("CREATE EXTENSION IF NOT EXISTS postgis;").await?;

    // Enable HSTORE extension
    pool.execute("CREATE EXTENSION IF NOT EXISTS hstore;").await?;

    // Create enum types
    pool.execute(
        r#"
        DO $$ BEGIN
            CREATE TYPE network_type AS ENUM ('individual', 'company');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        "#,
    )
    .await?;

    pool.execute(
        r#"
        DO $$ BEGIN
            CREATE TYPE current_type AS ENUM ('AC', 'DC');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        "#,
    )
    .await?;

    pool.execute(
        r#"
        DO $$ BEGIN
            CREATE TYPE connector_status AS ENUM ('available', 'occupied', 'out_of_service', 'reserved');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        "#,
    )
    .await?;

    pool.execute(
        r#"
        DO $$ BEGIN
            CREATE TYPE charging_session_status AS ENUM ('active', 'completed', 'cancelled', 'interrupted');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        "#,
    )
    .await?;

    pool.execute(
        r#"
        DO $$ BEGIN
            CREATE TYPE payment_status AS ENUM ('pending', 'paid', 'failed', 'refunded');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        "#,
    )
    .await?;

    pool.execute(
        r#"
        DO $$ BEGIN
            CREATE TYPE pricing_model AS ENUM ('per_kwh', 'per_minute', 'flat_rate', 'membership');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        "#,
    )
    .await?;

    pool.execute(
        r#"
        DO $$ BEGIN
            CREATE TYPE company_size AS ENUM ('small', 'medium', 'large');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;
        "#,
    )
    .await?;

    // Create tables
    sqlx::query(
        r#"
        CREATE TABLE IF NOT EXISTS networks (
            network_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            type network_type NOT NULL,
            contact_email VARCHAR(255),
            phone_number VARCHAR(50),
            address TEXT,
            created_by UUID NOT NULL,
            updated_by UUID,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        "#,
    )
    .execute(pool)
    .await?;

    sqlx::query(
        r#"
        CREATE TABLE IF NOT EXISTS companies (
            company_id SERIAL PRIMARY KEY,
            network_id INTEGER UNIQUE NOT NULL REFERENCES networks(network_id) ON DELETE CASCADE,
            business_registration_number VARCHAR(100),
            tax_id VARCHAR(100),
            company_size company_size,
            website_url VARCHAR(255),
            created_by UUID NOT NULL,
            updated_by UUID,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        "#,
    )
    .execute(pool)
    .await?;

    sqlx::query(
        r#"
        CREATE TABLE IF NOT EXISTS connector_types (
            connector_type_id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL UNIQUE,
            description TEXT,
            standard VARCHAR(100),
            current_type current_type NOT NULL,
            typical_power_kw DECIMAL(6, 2),
            pin_configuration VARCHAR(100),
            is_public_standard BOOLEAN DEFAULT TRUE,
            created_by UUID NOT NULL,
            updated_by UUID,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        "#,
    )
    .execute(pool)
    .await?;

    sqlx::query(
        r#"
        CREATE TABLE IF NOT EXISTS stations (
            station_id SERIAL PRIMARY KEY,
            network_id INTEGER NOT NULL REFERENCES networks(network_id) ON DELETE CASCADE,
            name VARCHAR(255) NOT NULL,
            address TEXT NOT NULL,
            city VARCHAR(100),
            state VARCHAR(100),
            country VARCHAR(100),
            postal_code VARCHAR(20),
            location GEOGRAPHY(Point, 4326) NOT NULL,
            tags HSTORE,
            osm_id BIGINT,
            is_operational BOOLEAN DEFAULT TRUE,
            created_by UUID NOT NULL,
            updated_by UUID,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        "#,
    )
    .execute(pool)
    .await?;

    sqlx::query(
        r#"
        CREATE TABLE IF NOT EXISTS connectors (
            connector_id SERIAL PRIMARY KEY,
            station_id INTEGER NOT NULL REFERENCES stations(station_id) ON DELETE CASCADE,
            connector_type_id INTEGER NOT NULL REFERENCES connector_types(connector_type_id),
            power_level_kw DECIMAL(6, 2) NOT NULL,
            status connector_status DEFAULT 'available',
            max_voltage INTEGER,
            max_amperage INTEGER,
            serial_number VARCHAR(100),
            manufacturer VARCHAR(100),
            model VARCHAR(100),
            installation_date DATE,
            last_maintenance_date DATE,
            created_by UUID NOT NULL,
            updated_by UUID,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        "#,
    )
    .execute(pool)
    .await?;

    sqlx::query(
        r#"
        CREATE TABLE IF NOT EXISTS charging_sessions (
            session_id SERIAL PRIMARY KEY,
            connector_id INTEGER NOT NULL REFERENCES connectors(connector_id),
            user_id UUID NOT NULL,
            start_time TIMESTAMP WITH TIME ZONE NOT NULL,
            end_time TIMESTAMP WITH TIME ZONE,
            energy_delivered_kwh DECIMAL(8, 2),
            total_cost DECIMAL(8, 2),
            payment_status payment_status DEFAULT 'pending',
            payment_method VARCHAR(50),
            session_status charging_session_status DEFAULT 'active',
            initiated_by UUID NOT NULL,
            ended_by UUID,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        "#,
    )
    .execute(pool)
    .await?;

    sqlx::query(
        r#"
        CREATE TABLE IF NOT EXISTS station_availability (
            availability_id SERIAL PRIMARY KEY,
            station_id INTEGER NOT NULL REFERENCES stations(station_id) ON DELETE CASCADE,
            day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6),
            open_time TIME,
            close_time TIME,
            is_24_hours BOOLEAN DEFAULT FALSE,
            created_by UUID NOT NULL,
            updated_by UUID,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        "#,
    )
    .execute(pool)
    .await?;

    sqlx::query(
        r#"
        CREATE TABLE IF NOT EXISTS pricing (
            pricing_id SERIAL PRIMARY KEY,
            network_id INTEGER NOT NULL REFERENCES networks(network_id),
            connector_type_id INTEGER REFERENCES connector_types(connector_type_id),
            pricing_model pricing_model NOT NULL,
            cost_per_kwh DECIMAL(8, 4),
            cost_per_minute DECIMAL(8, 4),
            flat_rate_cost DECIMAL(8, 2),
            membership_fee DECIMAL(8, 2),
            start_time TIME,
            end_time TIME,
            day_of_week INTEGER CHECK (day_of_week BETWEEN 0 AND 6),
            is_active BOOLEAN DEFAULT TRUE,
            effective_from DATE NOT NULL,
            effective_until DATE,
            created_by UUID NOT NULL,
            updated_by UUID,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        "#,
    )
    .execute(pool)
    .await?;

    sqlx::query(
        r#"
        CREATE TABLE IF NOT EXISTS api_audit_log (
            audit_id SERIAL PRIMARY KEY,
            user_id UUID NOT NULL,
            action VARCHAR(100) NOT NULL,
            resource_type VARCHAR(50) NOT NULL,
            resource_id INTEGER,
            ip_address INET,
            user_agent TEXT,
            request_method VARCHAR(10),
            status_code INTEGER,
            error_message TEXT,
            created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
        "#,
    )
    .execute(pool)
    .await?;

    // Create indexes
    sqlx::query("CREATE INDEX IF NOT EXISTS idx_stations_location ON stations USING GIST (location)")
        .execute(pool)
        .await?;

    sqlx::query("CREATE INDEX IF NOT EXISTS idx_stations_tags ON stations USING GIN (tags)")
        .execute(pool)
        .await?;

    sqlx::query("CREATE INDEX IF NOT EXISTS idx_stations_network ON stations(network_id)")
        .execute(pool)
        .await?;

    sqlx::query("CREATE INDEX IF NOT EXISTS idx_connectors_station ON connectors(station_id)")
        .execute(pool)
        .await?;

    sqlx::query("CREATE INDEX IF NOT EXISTS idx_connectors_status ON connectors(status)")
        .execute(pool)
        .await?;

    sqlx::query("CREATE INDEX IF NOT EXISTS idx_sessions_connector ON charging_sessions(connector_id)")
        .execute(pool)
        .await?;

    sqlx::query("CREATE INDEX IF NOT EXISTS idx_sessions_user ON charging_sessions(user_id)")
        .execute(pool)
        .await?;

    sqlx::query("CREATE INDEX IF NOT EXISTS idx_audit_user ON api_audit_log(user_id)")
        .execute(pool)
        .await?;

    Ok(())
}