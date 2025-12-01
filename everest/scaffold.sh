#!/bin/bash

set -e

PROJECT_NAME="configurator-service"

echo "Creating project structure for $PROJECT_NAME..."

cargo new $PROJECT_NAME
cd $PROJECT_NAME

cargo add actix-web
cargo add actix-cors
cargo add serde_json
cargo add async-trait
cargo add serde -F derive
cargo add chrono -F serde
cargo add futures-util
cargo add env_logger
cargo add dotenvy
cargo add uuid -F "serde v4"
cargo add sqlx -F "tls-native-tls runtime-async-std postgres chrono uuid"
cargo add jsonwebtoken 
cargo add argon2
cargo add validator -F derive
cargo add utoipa -F "chrono actix_extras"
cargo add utoipa-swagger-ui -F actix-web
