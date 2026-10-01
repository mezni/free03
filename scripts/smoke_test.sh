#!/usr/bin/env sh

set -eu

echo "Checking liveness..."

curl --fail \
    http://localhost:8000/health

echo

echo "Checking readiness..."

curl --fail \
    http://localhost:8000/health/ready

echo

echo "Smoke test passed."