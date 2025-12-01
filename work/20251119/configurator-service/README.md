# configurator-service

A comprehensive EV station management system built with Rust, Actix-web, and SQLx.

## Features

- Station management
- Connector management
- Network management
- User management
- Real-time status updates
- RESTful API with Swagger documentation

## Entities

- network

## Getting Started

1. Clone the repository
2. Set up environment variables (copy .env.example to .env)
3. Run database migrations: `./scripts/migrate.sh`
4. Start the server: `cargo run`

## API Documentation

Once running, access Swagger UI at: http://localhost:8080/swagger-ui/
