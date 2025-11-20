#!/bin/bash
set -e

echo "Running tests..."
cargo test --verbose
echo "Tests completed!"
