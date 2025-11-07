#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Service templates
declare -A SERVICE_TEMPLATES=(
    ["auth"]="Authentication service with JWT and Keycloak"
    ["api"]="REST API service with CRUD operations"
    ["worker"]="Background worker service with queue processing"
    ["gateway"]="API Gateway service with routing and rate limiting"
    ["microservice"]="Generic microservice with basic structure"
)

# Print colored output
log_info() { echo -e "${BLUE}ℹ ${NC}$1"; }
log_success() { echo -e "${GREEN}✅ ${NC}$1"; }
log_warning() { echo -e "${YELLOW}⚠ ${NC}$1"; }
log_error() { echo -e "${RED}❌ ${NC}$1"; }

# Show usage
show_usage() {
    echo "Usage: $0 <service-type> <service-name> [author] [email]"
    echo ""
    echo "Available service types:"
    for template in "${!SERVICE_TEMPLATES[@]}"; do
        echo "  $template - ${SERVICE_TEMPLATES[$template]}"
    done
    echo ""
    echo "Examples:"
    echo "  $0 auth user-auth-service \"John Doe\" \"john@example.com\""
    echo "  $0 api products-api"
    echo "  $0 worker email-worker"
    exit 1
}

# Validate inputs
validate_inputs() {
    if [ $# -lt 2 ]; then
        show_usage
    fi

    SERVICE_TYPE=$1
    SERVICE_NAME=$2
    AUTHOR=${3:-"$(git config user.name)"}
    EMAIL=${4:-"$(git config user.email)"}

    if [ -z "$AUTHOR" ]; then
        AUTHOR="Your Name"
    fi

    if [ -z "$EMAIL" ]; then
        EMAIL="your.email@example.com"
    fi

    if [[ ! "${!SERVICE_TEMPLATES[@]}" =~ "${SERVICE_TYPE}" ]]; then
        log_error "Unknown service type: $SERVICE_TYPE"
        show_usage
    fi

    if [[ ! "$SERVICE_NAME" =~ ^[a-z0-9-]+$ ]]; then
        log_error "Service name must be lowercase with hyphens only"
        exit 1
    fi
}

# Create directory structure
create_directories() {
    log_info "Creating directory structure for $SERVICE_NAME..."

    local dirs=(
        "src/domain"
        "src/application" 
        "src/infrastructure"
        "src/api"
        "scripts"
        "deployments/docker"
        "deployments/kubernetes"
        "config"
        "openapi"
        "tools"
        "tests"
        "docs"
        "migrations"
    )

    for dir in "${dirs[@]}"; do
        mkdir -p "$SERVICE_NAME/$dir"
    done
}

# Generate Cargo.toml based on service type
generate_cargo_toml() {
    local service_type=$1
    local service_name=$2
    local author=$3
    local email=$4

    log_info "Generating Cargo.toml for $service_type service..."

    local common_deps=(
        "tokio = { version = \"1.0\", features = [\"full\"] }"
        "serde = { version = \"1.0\", features = [\"derive\"] }"
        "serde_json = \"1.0\""
        "async-trait = \"0.1\""
        "thiserror = \"1.0\""
        "config = \"0.13\""
        "log = \"0.4\""
        "env_logger = \"0.10\""
    )

    local type_specific_deps=()
    local type_specific_features=()

    case $service_type in
        "auth")
            type_specific_deps=(
                "actix-web = \"4.4\""
                "jsonwebtoken = \"8.0\""
                "bcrypt = \"0.15\""
                "uuid = { version = \"1.0\", features = [\"v4\", \"serde\"] }"
                "validator = { version = \"0.16\", features = [\"derive\"] }"
                "reqwest = { version = \"0.11\", features = [\"json\"] }"
                "utoipa = { version = \"3.0\", features = [\"actix_extras\"] }"
                "utoipa-swagger-ui = { version = \"3.0\", features = [\"actix-web\"] }"
            )
            ;;
        "api")
            type_specific_deps=(
                "actix-web = \"4.4\""
                "sqlx = { version = \"0.7\", features = [\"postgres\", \"runtime-tokio-native-tls\"] }"
                "uuid = { version = \"1.0\", features = [\"v4\", \"serde\"] }"
                "validator = { version = \"0.16\", features = [\"derive\"] }"
                "utoipa = { version = \"3.0\", features = [\"actix_extras\"] }"
                "utoipa-swagger-ui = { version = \"3.0\", features = [\"actix-web\"] }"
            )
            ;;
        "worker")
            type_specific_deps=(
                "redis = { version = \"0.23\", features = [\"tokio-comp\"] }"
                "sqlx = { version = \"0.7\", features = [\"postgres\", \"runtime-tokio-native-tls\"] }"
                "chrono = { version = \"0.4\", features = [\"serde\"] }"
            )
            ;;
        "gateway")
            type_specific_deps=(
                "actix-web = \"4.4\""
                "reqwest = { version = \"0.11\", features = [\"json\"] }"
                "uuid = { version = \"1.0\", features = [\"v4\", \"serde\"] }"
                " governor = \"0.6\""
            )
            ;;
        "microservice")
            type_specific_deps=(
                "actix-web = \"4.4\""
                "utoipa = { version = \"3.0\", features = [\"actix_extras\"] }"
                "utoipa-swagger-ui = { version = \"3.0\", features = [\"actix-web\"] }"
            )
            ;;
    esac

    cat > "$SERVICE_NAME/Cargo.toml" << EOF
[package]
name = "$service_name"
version = "0.1.0"
edition = "2021"
description = "$service_type service generated by Rust Service Generator"
authors = ["$author <$email>"]
license = "MIT"
repository = "https://github.com/your-org/$service_name"
readme = "README.md"

[dependencies]
$(printf "%s\n" "${common_deps[@]}")
$(printf "%s\n" "${type_specific_deps[@]}")

[dev-dependencies]
actix-rt = "2.0"
mockito = "1.0"

[profile.dev]
opt-level = 0
debug = true

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
panic = 'abort'
EOF
}

# Generate main.rs based on service type
generate_main_rs() {
    local service_type=$1
    local service_name=$2

    log_info "Generating main.rs for $service_type service..."

    case $service_type in
        "auth"|"api"|"gateway"|"microservice")
            cat > "$SERVICE_NAME/src/main.rs" << 'EOF'
mod domain;
mod application;
mod infrastructure;
mod api;

use config::Config;
use log::info;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    // Initialize logging
    env_logger::init();
    
    // Load configuration
    let config = Config::builder()
        .add_source(config::File::with_name("config/default"))
        .add_source(config::Environment::with_prefix("APP"))
        .build()
        .expect("Failed to load configuration");

    let host = config.get_string("server.host").unwrap_or_else(|_| "127.0.0.1".to_string());
    let port = config.get_string("server.port").unwrap_or_else(|_| "8080".to_string());
    let bind_address = format!("{}:{}", host, port);

    info!("Starting {} on {}", env!("CARGO_PKG_NAME"), bind_address);

    // Start HTTP server
    actix_web::HttpServer::new(|| {
        actix_web::App::new()
            .configure(api::routes::configure_routes)
    })
    .bind(bind_address)?
    .run()
    .await
}
EOF
            ;;
        "worker")
            cat > "$SERVICE_NAME/src/main.rs" << 'EOF'
mod domain;
mod application;
mod infrastructure;

use config::Config;
use log::info;

#[tokio::main]
async fn main() {
    // Initialize logging
    env_logger::init();
    
    // Load configuration
    let config = Config::builder()
        .add_source(config::File::with_name("config/default"))
        .add_source(config::Environment::with_prefix("APP"))
        .build()
        .expect("Failed to load configuration");

    info!("Starting {} worker service", env!("CARGO_PKG_NAME"));

    // Main worker loop
    loop {
        tokio::time::sleep(tokio::time::Duration::from_secs(1)).await;
    }
}
EOF
            ;;
    esac
}

# Generate domain files
generate_domain_files() {
    local service_type=$1

    log_info "Generating domain layer..."

    # mod.rs
    cat > "$SERVICE_NAME/src/domain/mod.rs" << 'EOF'
pub mod entities;
pub mod value_objects;
pub mod traits;
pub mod errors;
pub mod events;
EOF

    # errors.rs
    cat > "$SERVICE_NAME/src/domain/errors.rs" << EOF
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DomainError {
    #[error("Validation error: {0}")]
    ValidationError(String),
    
    #[error("Not found: {0}")]
    NotFound(String),
    
    #[error("Already exists: {0}")]
    AlreadyExists(String),
    
    #[error("Authentication failed: {0}")]
    AuthenticationFailed(String),
    
    #[error("Authorization failed: {0}")]
    AuthorizationFailed(String),
    
    #[error("Internal error: {0}")]
    InternalError(String),
}
EOF

    # Generate service-specific entities
    case $service_type in
        "auth")
            cat > "$SERVICE_NAME/src/domain/entities.rs" << 'EOF'
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct User {
    pub id: Uuid,
    pub username: String,
    pub email: String,
    pub password_hash: String,
    pub enabled: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Role {
    pub id: Uuid,
    pub name: String,
    pub permissions: Vec<Permission>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Permission {
    pub id: Uuid,
    pub name: String,
    pub resource: String,
    pub action: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Token {
    pub access_token: String,
    pub refresh_token: String,
    pub expires_in: i64,
}
EOF
            ;;
        "api")
            cat > "$SERVICE_NAME/src/domain/entities.rs" << 'EOF'
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Entity {
    pub id: Uuid,
    pub name: String,
    pub description: Option<String>,
    pub created_at: chrono::DateTime<chrono::Utc>,
    pub updated_at: chrono::DateTime<chrono::Utc>,
}
EOF
            ;;
        *)
            cat > "$SERVICE_NAME/src/domain/entities.rs" << 'EOF'
use serde::{Deserialize, Serialize};
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BaseEntity {
    pub id: Uuid,
    pub created_at: chrono::DateTime<chrono::Utc>,
    pub updated_at: chrono::DateTime<chrono::Utc>,
}
EOF
            ;;
    esac
}

# Generate configuration files
generate_config_files() {
    local service_type=$1

    log_info "Generating configuration files..."

    # default.toml
    cat > "$SERVICE_NAME/config/default.toml" << EOF
[server]
host = "0.0.0.0"
port = 8080
workers = 4

[log]
level = "info"
format = "json"

[database]
url = "\${DATABASE_URL}"
max_connections = 20

[redis]
url = "\${REDIS_URL}"

[health_check]
enabled = true
endpoint = "/health"
EOF

    # development.toml
    cat > "$SERVICE_NAME/config/development.toml" << EOF
[server]
host = "127.0.0.1"
port = 8080

[log]
level = "debug"
format = "pretty"

[database]
url = "postgresql://postgres:password@localhost:5432/${SERVICE_NAME}_dev"

[redis]
url = "redis://localhost:6379"
EOF

    # production.toml
    cat > "$SERVICE_NAME/config/production.toml" << EOF
[server]
host = "0.0.0.0"
port = 8080
workers = 8

[log]
level = "warn"
format = "json"

[database]
url = "\${DATABASE_URL}"
max_connections = 50

[redis]
url = "\${REDIS_URL}"
EOF
}

# Generate Dockerfile
generate_dockerfile() {
    local service_type=$1
    local service_name=$2

    log_info "Generating Dockerfile..."

    cat > "$SERVICE_NAME/deployments/docker/Dockerfile" << EOF
# Multi-stage build
FROM rust:1.70-alpine as builder

RUN apk add --no-cache musl-dev openssl-dev openssl pkgconfig

WORKDIR /app

COPY Cargo.toml Cargo.lock ./
COPY src ./src

RUN cargo build --release

FROM alpine:3.18

RUN apk add --no-cache openssl ca-certificates && \\
    update-ca-certificates

RUN addgroup -g 1000 -S app && \\
    adduser -u 1000 -S app -G app

WORKDIR /app

COPY --from=builder /app/target/release/${service_name} /app/${service_name}
COPY config ./config

RUN chown -R app:app /app

USER app

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["/app/${service_name}"]
EOF
}

# Generate scripts
generate_scripts() {
    local service_name=$2

    log_info "Generating utility scripts..."

    # run.sh
    cat > "$SERVICE_NAME/scripts/run.sh" << EOF
#!/bin/bash

set -e

ENV=\${1:-development}

echo "Starting $service_name in \$ENV mode..."

export RUST_LOG=debug
export CONFIG_FILE=config/\$ENV.toml

if [ "\$ENV" = "production" ]; then
    cargo build --release
    ./target/release/$service_name
else
    cargo run
fi
EOF

    # test.sh
    cat > "$SERVICE_NAME/scripts/test.sh" << 'EOF'
#!/bin/bash

set -e

echo "Running tests..."

cargo test
cargo clippy -- -D warnings
cargo fmt -- --check

echo "All tests passed! ✅"
EOF

    # build.sh
    cat > "$SERVICE_NAME/scripts/build.sh" << EOF
#!/bin/bash

set -e

echo "Building $service_name..."

if [ "\$1" = "production" ]; then
    cargo build --release
    strip target/release/$service_name
elif [ "\$1" = "docker" ]; then
    docker build -t $service_name:latest -f deployments/docker/Dockerfile .
else
    cargo build
fi
EOF

    # deploy.sh
    cat > "$SERVICE_NAME/scripts/deploy.sh" << 'EOF'
#!/bin/bash

set -e

ENVIRONMENT=${1:-staging}

echo "Deploying to $ENVIRONMENT..."

case $ENVIRONMENT in
    development)
        docker-compose -f deployments/docker/docker-compose.yml up -d
        ;;
    staging|production)
        kubectl apply -k deployments/kubernetes/overlays/$ENVIRONMENT
        kubectl rollout status deployment/$service_name
        ;;
    *)
        echo "Unknown environment: $ENVIRONMENT"
        exit 1
        ;;
esac

echo "Deployment completed! 🚀"
EOF

    # Make scripts executable
    chmod +x "$SERVICE_NAME/scripts/"*.sh
}

# Generate README.md
generate_readme() {
    local service_type=$1
    local service_name=$2
    local author=$3

    log_info "Generating README.md..."

    cat > "$SERVICE_NAME/README.md" << EOF
# $service_name

${SERVICE_TEMPLATES[$service_type]}

## Quick Start

\`\`\`bash
# Run in development mode
./scripts/run.sh development

# Run tests
./scripts/test.sh

# Build for production
./scripts/build.sh production
\`\`\`

## Project Structure

\`\`\`
$service_name/
├── src/                 # Source code
├── scripts/             # Utility scripts
├── deployments/         # Deployment configurations
├── config/              # Configuration files
├── tests/               # Integration tests
└── docs/                # Documentation
\`\`\`

## Development

\`\`\`bash
# Format code
cargo fmt

# Run clippy
cargo clippy

# Run tests
cargo test
\`\`\`

## Deployment

\`\`\`bash
# Deploy to development
./scripts/deploy.sh development

# Deploy to production
./scripts/deploy.sh production
\`\`\`

## License

MIT
EOF
}

# Generate .env.example
generate_env_example() {
    cat > "$SERVICE_NAME/.env.example" << 'EOF'
# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8080
RUST_LOG=debug

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379

# JWT (for auth services)
JWT_SECRET=your-jwt-secret-here
EOF
}

# Generate .gitignore
generate_gitignore() {
    cat > "$SERVICE_NAME/.gitignore" << 'EOF'
# Generated by Cargo
/target/

# Environment variables
.env
*.env

# OS generated files
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo
EOF
}

# Generate docker-compose.yml
generate_docker_compose() {
    local service_name=$1

    cat > "$SERVICE_NAME/deployments/docker/docker-compose.yml" << EOF
version: '3.8'

services:
  $service_name:
    build:
      context: ../..
      dockerfile: deployments/docker/Dockerfile
    ports:
      - "8080:8080"
    environment:
      - RUST_LOG=debug
      - CONFIG_FILE=config/development.toml
    volumes:
      - ../../config:/app/config:ro
    depends_on:
      - postgres
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=${service_name}_dev
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
EOF
}

# Main function
main() {
    echo -e "${BLUE}🚀 Rust Service Generator${NC}"
    echo "=========================="

    validate_inputs "$@"

    log_info "Generating $SERVICE_TYPE service: $SERVICE_NAME"
    log_info "Author: $AUTHOR <$EMAIL>"

    # Check if service directory already exists
    if [ -d "$SERVICE_NAME" ]; then
        log_warning "Directory $SERVICE_NAME already exists!"
        read -p "Do you want to overwrite it? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_error "Aborted."
            exit 1
        fi
        rm -rf "$SERVICE_NAME"
    fi

    # Generate service structure
    create_directories
    generate_cargo_toml "$SERVICE_TYPE" "$SERVICE_NAME" "$AUTHOR" "$EMAIL"
    generate_main_rs "$SERVICE_TYPE" "$SERVICE_NAME"
    generate_domain_files "$SERVICE_TYPE"
    generate_config_files "$SERVICE_TYPE"
    generate_dockerfile "$SERVICE_TYPE" "$SERVICE_NAME"
    generate_scripts "$SERVICE_TYPE" "$SERVICE_NAME"
    generate_readme "$SERVICE_TYPE" "$SERVICE_NAME" "$AUTHOR"
    generate_env_example
    generate_gitignore
    generate_docker_compose "$SERVICE_NAME"

    log_success "Service $SERVICE_NAME generated successfully!"
    echo ""
    echo -e "${GREEN}Quick start:${NC}"
    echo "  cd $SERVICE_NAME"
    echo "  ./scripts/run.sh development"
    echo ""
    echo -e "${GREEN}Docker development:${NC}"
    echo "  docker-compose -f deployments/docker/docker-compose.yml up -d"
    echo ""
    echo -e "${GREEN}Available scripts:${NC}"
    echo "  ./scripts/run.sh [env]     - Run service"
    echo "  ./scripts/test.sh          - Run tests"
    echo "  ./scripts/build.sh [type]  - Build service"
    echo "  ./scripts/deploy.sh [env]  - Deploy service"
}

# Run main function with all arguments
main "$@"