#!/bin/bash

set -e

echo "Building auth-service..."

if [ "$1" = "production" ]; then
    cargo build --release
    strip target/release/auth-service
elif [ "$1" = "docker" ]; then
    docker build -t auth-service:latest -f deployments/docker/Dockerfile .
else
    cargo build
fi
