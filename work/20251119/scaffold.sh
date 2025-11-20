#!/bin/bash

set -e

# Configuration
PROJECT_NAME="configurator-service"
AUTHOR="M.MEZNI <mamezni@gmail.com>"

# Define your entities here - add or remove as needed
ENTITIES=("station" "connector" "network" "company" "individual" "person")

echo "Creating $PROJECT_NAME project structure..."

# Create main directories
mkdir -p ${PROJECT_NAME}/{src,tests,docs,scripts}
mkdir -p ${PROJECT_NAME}/src/{domain,application,infrastructure,api,utils}
mkdir -p ${PROJECT_NAME}/tests/{unit,integration}

# Create domain subdirectories
mkdir -p ${PROJECT_NAME}/src/domain/{models,value_objects,enums,events,services}
mkdir -p ${PROJECT_NAME}/src/domain/models
mkdir -p ${PROJECT_NAME}/src/domain/value_objects
mkdir -p ${PROJECT_NAME}/src/domain/enums
mkdir -p ${PROJECT_NAME}/src/domain/events
mkdir -p ${PROJECT_NAME}/src/domain/services

# Create application subdirectories
mkdir -p ${PROJECT_NAME}/src/application/{commands,queries,handlers,dtos}
mkdir -p ${PROJECT_NAME}/src/application/commands
mkdir -p ${PROJECT_NAME}/src/application/queries
mkdir -p ${PROJECT_NAME}/src/application/handlers
mkdir -p ${PROJECT_NAME}/src/application/dtos

# Create infrastructure subdirectories
mkdir -p ${PROJECT_NAME}/src/infrastructure/{database,config,external}
mkdir -p ${PROJECT_NAME}/src/infrastructure/database/{repositories,migrations}
mkdir -p ${PROJECT_NAME}/src/infrastructure/database/repositories

# Create API subdirectories
mkdir -p ${PROJECT_NAME}/src/api/{routes,handlers,middleware,responses}
mkdir -p ${PROJECT_NAME}/src/api/routes
mkdir -p ${PROJECT_NAME}/src/api/handlers
mkdir -p ${PROJECT_NAME}/src/api/middleware
mkdir -p ${PROJECT_NAME}/src/api/responses

# Create root files
touch ${PROJECT_NAME}/Cargo.toml
touch ${PROJECT_NAME}/Cargo.lock
touch ${PROJECT_NAME}/.env
touch ${PROJECT_NAME}/.gitignore
touch ${PROJECT_NAME}/README.md

# Create source files
touch ${PROJECT_NAME}/src/main.rs
touch ${PROJECT_NAME}/src/lib.rs

# Create domain model files for each entity
touch ${PROJECT_NAME}/src/domain/mod.rs
touch ${PROJECT_NAME}/src/domain/models/mod.rs

for entity in "${ENTITIES[@]}"; do
    echo "Creating files for entity: $entity"
    touch "${PROJECT_NAME}/src/domain/models/${entity}.rs"
done

# Create value objects
touch ${PROJECT_NAME}/src/domain/value_objects/mod.rs
touch ${PROJECT_NAME}/src/domain/value_objects/location.rs
touch ${PROJECT_NAME}/src/domain/value_objects/contact_info.rs
touch ${PROJECT_NAME}/src/domain/value_objects/tags.rs
touch ${PROJECT_NAME}/src/domain/value_objects/operational_status.rs
touch ${PROJECT_NAME}/src/domain/value_objects/verification_status.rs
touch ${PROJECT_NAME}/src/domain/value_objects/email.rs
touch ${PROJECT_NAME}/src/domain/value_objects/phone.rs

# Create enums
touch ${PROJECT_NAME}/src/domain/enums/mod.rs
touch ${PROJECT_NAME}/src/domain/enums/network_type.rs
touch ${PROJECT_NAME}/src/domain/enums/company_type.rs
touch ${PROJECT_NAME}/src/domain/enums/role_type.rs
touch ${PROJECT_NAME}/src/domain/enums/connector_status.rs

# Create event files for each entity
touch ${PROJECT_NAME}/src/domain/events/mod.rs

for entity in "${ENTITIES[@]}"; do
    if [[ "$entity" == "station" || "$entity" == "connector" || "$entity" == "network" ]]; then
        touch "${PROJECT_NAME}/src/domain/events/${entity}_events.rs"
    fi
done

# Create service files
touch ${PROJECT_NAME}/src/domain/services/mod.rs
touch ${PROJECT_NAME}/src/domain/services/station_service.rs
touch ${PROJECT_NAME}/src/domain/services/network_service.rs
touch ${PROJECT_NAME}/src/domain/services/verification_service.rs

# Create application files
touch ${PROJECT_NAME}/src/application/mod.rs

# Create command files for each entity
touch ${PROJECT_NAME}/src/application/commands/mod.rs

for entity in "${ENTITIES[@]}"; do
    if [[ "$entity" == "station" || "$entity" == "connector" || "$entity" == "network" ]]; then
        touch "${PROJECT_NAME}/src/application/commands/${entity}_commands.rs"
    fi
done

# Create query files for each entity
touch ${PROJECT_NAME}/src/application/queries/mod.rs

for entity in "${ENTITIES[@]}"; do
    if [[ "$entity" == "station" || "$entity" == "connector" || "$entity" == "network" ]]; then
        touch "${PROJECT_NAME}/src/application/queries/${entity}_queries.rs"
    fi
done

# Create handler files
touch ${PROJECT_NAME}/src/application/handlers/mod.rs
touch ${PROJECT_NAME}/src/application/handlers/command_handlers.rs
touch ${PROJECT_NAME}/src/application/handlers/query_handlers.rs

# Create DTO files for each entity
touch ${PROJECT_NAME}/src/application/dtos/mod.rs

for entity in "${ENTITIES[@]}"; do
    if [[ "$entity" == "station" || "$entity" == "connector" || "$entity" == "network" ]]; then
        touch "${PROJECT_NAME}/src/application/dtos/${entity}_dtos.rs"
    fi
done

# Create infrastructure files
touch ${PROJECT_NAME}/src/infrastructure/mod.rs
touch ${PROJECT_NAME}/src/infrastructure/database/mod.rs
touch ${PROJECT_NAME}/src/infrastructure/database/connection.rs

# Create repository files for each entity
touch ${PROJECT_NAME}/src/infrastructure/database/repositories/mod.rs

for entity in "${ENTITIES[@]}"; do
    if [[ "$entity" == "station" || "$entity" == "connector" || "$entity" == "network" || "$entity" == "person" ]]; then
        touch "${PROJECT_NAME}/src/infrastructure/database/repositories/${entity}_repository.rs"
    fi
done

touch ${PROJECT_NAME}/src/infrastructure/database/migrations/mod.rs
touch ${PROJECT_NAME}/src/infrastructure/database/migrations/001_initial_schema.sql

touch ${PROJECT_NAME}/src/infrastructure/config/mod.rs
touch ${PROJECT_NAME}/src/infrastructure/config/settings.rs

touch ${PROJECT_NAME}/src/infrastructure/external/mod.rs
touch ${PROJECT_NAME}/src/infrastructure/external/email_service.rs
touch ${PROJECT_NAME}/src/infrastructure/external/sms_service.rs

# Create API route files for each entity
touch ${PROJECT_NAME}/src/api/mod.rs
touch ${PROJECT_NAME}/src/api/routes/mod.rs

for entity in "${ENTITIES[@]}"; do
    if [[ "$entity" == "station" || "$entity" == "connector" || "$entity" == "network" || "$entity" == "person" ]]; then
        touch "${PROJECT_NAME}/src/api/routes/${entity}s.rs"
    fi
done

# Create API handler files for each entity
touch ${PROJECT_NAME}/src/api/handlers/mod.rs

for entity in "${ENTITIES[@]}"; do
    if [[ "$entity" == "station" || "$entity" == "connector" || "$entity" == "network" ]]; then
        touch "${PROJECT_NAME}/src/api/handlers/${entity}_handlers.rs"
    fi
done

# Create middleware files
touch ${PROJECT_NAME}/src/api/middleware/mod.rs
touch ${PROJECT_NAME}/src/api/middleware/auth.rs
touch ${PROJECT_NAME}/src/api/middleware/logging.rs
touch ${PROJECT_NAME}/src/api/middleware/error_handling.rs

# Create response files
touch ${PROJECT_NAME}/src/api/responses/mod.rs
touch ${PROJECT_NAME}/src/api/responses/api_response.rs
touch ${PROJECT_NAME}/src/api/responses/error_response.rs

# Create utils files
touch ${PROJECT_NAME}/src/utils/mod.rs
touch ${PROJECT_NAME}/src/utils/validators.rs
touch ${PROJECT_NAME}/src/utils/datetime.rs
touch ${PROJECT_NAME}/src/utils/id_generator.rs

# Create test files
touch ${PROJECT_NAME}/tests/mod.rs
touch ${PROJECT_NAME}/tests/unit/mod.rs
touch ${PROJECT_NAME}/tests/unit/domain_tests.rs
touch ${PROJECT_NAME}/tests/unit/service_tests.rs
touch ${PROJECT_NAME}/tests/integration/mod.rs

# Create integration test files for main entities
for entity in "${ENTITIES[@]}"; do
    if [[ "$entity" == "station" || "$entity" == "network" ]]; then
        touch "${PROJECT_NAME}/tests/integration/${entity}_tests.rs"
    fi
done

# Create docs files
touch ${PROJECT_NAME}/docs/api.md
touch ${PROJECT_NAME}/docs/architecture.md
touch ${PROJECT_NAME}/docs/deployment.md

# Create script files
touch ${PROJECT_NAME}/scripts/migrate.sh
touch ${PROJECT_NAME}/scripts/test.sh
touch ${PROJECT_NAME}/scripts/deploy.sh

# Make scripts executable
chmod +x ${PROJECT_NAME}/scripts/migrate.sh
chmod +x ${PROJECT_NAME}/scripts/test.sh
chmod +x ${PROJECT_NAME}/scripts/deploy.sh

# Create basic Cargo.toml content
cat > ${PROJECT_NAME}/Cargo.toml << EOF
[package]
name = "${PROJECT_NAME}"
version = "0.1.0"
edition = "2021"
description = "EV Station Management System"
authors = ["${AUTHOR}"]
license = "MIT"

[dependencies]
actix-web = "4.4"
actix-cors = "0.7"
tokio = { version = "1.0", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
sqlx = { version = "0.7", features = ["postgres", "runtime-tokio-rustls"] }
chrono = { version = "0.4", features = ["serde"] }
uuid = { version = "1.0", features = ["v4", "serde"] }
config = "0.13"
dotenvy = "0.15"
thiserror = "1.0"
log = "0.4"
env_logger = "0.10"
utoipa = { version = "3.0", features = ["actix_extras"] }
utoipa-swagger-ui = { version = "3.0", features = ["actix-web"] }
validator = { version = "0.16", features = ["derive"] }
argon2 = "0.5"
jsonwebtoken = "8.3"

[dev-dependencies]
rstest = "0.18"
mockall = "0.11"
testcontainers = "0.15"
EOF

# Create basic .gitignore
cat > ${PROJECT_NAME}/.gitignore << 'EOF'
/target/
**/*.rs.bk
.env
!.env.example
*.log
.DS_Store
.idea/
.vscode/
EOF

# Create basic README.md
cat > ${PROJECT_NAME}/README.md << EOF
# ${PROJECT_NAME}

A comprehensive EV station management system built with Rust, Actix-web, and SQLx.

## Features

- Station management
- Connector management
- Network management
- User management
- Real-time status updates
- RESTful API with Swagger documentation

## Entities

$(for entity in "${ENTITIES[@]}"; do
  echo "- ${entity}"
done)

## Getting Started

1. Clone the repository
2. Set up environment variables (copy .env.example to .env)
3. Run database migrations: \`./scripts/migrate.sh\`
4. Start the server: \`cargo run\`

## API Documentation

Once running, access Swagger UI at: http://localhost:8080/swagger-ui/
EOF

# Create basic .env file
cat > ${PROJECT_NAME}/.env << EOF
DATABASE_URL=postgres://user:password@localhost:5432/${PROJECT_NAME}
DATABASE_URL_TEST=postgres://user:password@localhost:5432/${PROJECT_NAME}_test
SERVER_HOST=127.0.0.1
SERVER_PORT=8080
RUST_LOG=debug
JWT_SECRET=your_jwt_secret_key_here
EOF

# Create basic script files
cat > ${PROJECT_NAME}/scripts/migrate.sh << 'EOF'
#!/bin/bash
set -e

echo "Running database migrations..."
# Add your migration commands here
# sqlx migrate run --database-url your_database_url
echo "Migrations completed!"
EOF

cat > ${PROJECT_NAME}/scripts/test.sh << 'EOF'
#!/bin/bash
set -e

echo "Running tests..."
cargo test --verbose
echo "Tests completed!"
EOF

cat > ${PROJECT_NAME}/scripts/deploy.sh << 'EOF'
#!/bin/bash
set -e

echo "Deploying application..."
# Add your deployment commands here
echo "Deployment completed!"
EOF

echo "Project structure for '${PROJECT_NAME}' created successfully!"
echo "Entities created: ${ENTITIES[*]}"
echo "Navigate to ${PROJECT_NAME}/ and run 'cargo build' to get started."