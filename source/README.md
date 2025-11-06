docker compose -f docker-compose.yml up -d

Keycloak: https://localhost:8443

Tyk Gateway: http://localhost:8080




┌───────────────────────┐
│       API / HTTP       │  <- Actix Web handlers, REST/GraphQL endpoints
├───────────────────────┤
│     Application Layer  │  <- Use Cases / Services
├───────────────────────┤
│   Domain Layer (Core)  │  <- Entities: User, Role, Permission, Token
├───────────────────────┤
│ Infrastructure Layer   │  <- Repos, Keycloak client, cache, database
└───────────────────────┘

Key Concepts

Entities (Domain)

User → ID, username, email

Role → admin, user, etc.

Permission → fine-grained access

Token → JWT or opaque token

Use Cases (Application)

AuthenticateUser → validate credentials via Keycloak

GenerateToken → create JWT for microservices

ValidateToken → check JWT signature, expiration, and roles

GetRolesAndPermissions → fetch user roles/permissions (from Keycloak + cache)

Infrastructure

KeycloakClient → talks to Keycloak Admin API

Cache → Redis or in-memory for tokens & roles

Database → optional local storage for audit/logging

auth-service/
├── Cargo.toml
├── src/
│   ├── main.rs              # Actix Web server entry
│   ├── api/                 # HTTP handlers
│   │   ├── auth.rs
│   │   └── user.rs
│   ├── application/         # Use cases / services
│   │   ├── auth_service.rs
│   │   └── role_service.rs
│   ├── domain/              # Entities
│   │   ├── user.rs
│   │   ├── role.rs
│   │   └── permission.rs
│   ├── infrastructure/
│   │   ├── keycloak.rs
│   │   ├── cache.rs
│   │   └── repository.rs
│   └── config.rs            # Config & secrets management


