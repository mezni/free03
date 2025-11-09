# configurator-service

REST API service with CRUD operations

## Quick Start

```bash
# Run in development mode
./scripts/run.sh development

# Run tests
./scripts/test.sh

# Build for production
./scripts/build.sh production
```

## Project Structure

```
configurator-service/
├── src/                 # Source code
├── scripts/             # Utility scripts
├── deployments/         # Deployment configurations
├── config/              # Configuration files
├── tests/               # Integration tests
└── docs/                # Documentation
```

## Development

```bash
# Format code
cargo fmt

# Run clippy
cargo clippy

# Run tests
cargo test
```

## Deployment

```bash
# Deploy to development
./scripts/deploy.sh development

# Deploy to production
./scripts/deploy.sh production
```

## License

MIT
