#!/bin/bash

set -e

ENV=${1:-development}

echo "Starting auth-service in $ENV mode..."

export RUST_LOG=debug
export CONFIG_FILE=config/$ENV.toml

if [ "$ENV" = "production" ]; then
    cargo build --release
    ./target/release/auth-service
else
    cargo run
fi
