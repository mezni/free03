#!/bin/bash

# Get the project name from the user
#read -p "Enter the project name: " PROJECT_NAME

PROJECT_NAME=auth-service

cargo new $PROJECT_NAME

# Create the application directory
mkdir -p $PROJECT_NAME/src/application
mkdir -p $PROJECT_NAME/src/application/command_handlers
mkdir -p $PROJECT_NAME/src/application/event_handlers

# Create the domain directory
mkdir -p $PROJECT_NAME/src/domain
mkdir -p $PROJECT_NAME/src/domain/entities
mkdir -p $PROJECT_NAME/src/domain/value_objects
mkdir -p $PROJECT_NAME/src/domain/repositories

# Create the infrastructure directory
mkdir -p $PROJECT_NAME/src/infrastructure
mkdir -p $PROJECT_NAME/src/infrastructure/database
mkdir -p $PROJECT_NAME/src/infrastructure/messaging

# Create the interface directory
mkdir -p $PROJECT_NAME/src/interface
mkdir -p $PROJECT_NAME/src/interface/http
mkdir -p $PROJECT_NAME/src/interface/grpc

# Create the tests directory
mkdir -p $PROJECT_NAME/tests
mkdir -p $PROJECT_NAME/tests/integration
mkdir -p $PROJECT_NAME/tests/unit

# Create the scripts directory
mkdir -p $PROJECT_NAME/scripts

# Create the deployment directory
mkdir -p $PROJECT_NAME/deployment
mkdir -p $PROJECT_NAME/deployment/docker
mkdir -p $PROJECT_NAME/deployment/kubernetes
mkdir -p $PROJECT_NAME/deployment/terraform

# Create the config directory
mkdir -p $PROJECT_NAME/config

# Create the docs directory
mkdir -p $PROJECT_NAME/docs
mkdir -p $PROJECT_NAME/docs/img

# Create the files
touch $PROJECT_NAME/Cargo.toml
touch $PROJECT_NAME/src/main.rs
touch $PROJECT_NAME/src/application/mod.rs
touch $PROJECT_NAME/src/domain/mod.rs
touch $PROJECT_NAME/src/infrastructure/mod.rs
touch $PROJECT_NAME/src/interface/http/user_controller.rs
touch $PROJECT_NAME/src/interface/grpc/user_service.rs
touch $PROJECT_NAME/scripts/build.sh
touch $PROJECT_NAME/scripts/deploy.sh
touch $PROJECT_NAME/scripts/run.sh
touch $PROJECT_NAME/scripts/test.sh
touch $PROJECT_NAME/deployment/docker/Dockerfile
touch $PROJECT_NAME/deployment/docker/docker-compose.yml
touch $PROJECT_NAME/deployment/kubernetes/deployment.yaml
touch $PROJECT_NAME/deployment/kubernetes/service.yaml
touch $PROJECT_NAME/deployment/terraform/main.tf
touch $PROJECT_NAME/config/development.toml
touch $PROJECT_NAME/config/production.toml
touch $PROJECT_NAME/config/staging.toml
touch $PROJECT_NAME/docs/api.md
touch $PROJECT_NAME/docs/architecture.md
touch $PROJECT_NAME/README.md

echo "Directory structure created successfully for $PROJECT_NAME!"