#!/bin/bash

set -e

echo "Building configurator-service..."

if [ "$1" = "production" ]; then
    cargo build --release
    strip target/release/configurator-service
elif [ "$1" = "docker" ]; then
    docker build -t configurator-service:latest -f deployments/docker/Dockerfile .
else
    cargo build
fi
