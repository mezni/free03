#!/bin/bash

set -e

echo "Running tests..."

cargo test
cargo clippy -- -D warnings
cargo fmt -- --check

echo "All tests passed! ✅"
