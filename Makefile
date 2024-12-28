# Go settings
GO            = go
GOBUILD       = $(GO) build
GOCLEAN       = $(GO) clean
GOTEST        = $(GO) test
GOGET         = $(GO) get
GOFMT         = $(GO) fmt
GOVET         = $(GO) vet

# Binaries and source
BIN           = bin
CDRCFG        = $(BIN)/cdrcfg
CDRGEN        = $(BIN)/cdrgen
SRC_CDRCFG    = cdrgen/cmd/cdrcfg/main.go
SRC_CDRGEN    = cdrgen/cmd/cdrgen/main.go

# Version (default)
VERSION       = 0.0.1

# Dependencies
DEPENDENCIES  = github.com/google/uuid gopkg.in/yaml.v3 go.etcd.io/bbolt github.com/stretchr/testify/assert

# Default target
all: install build

# Install dependencies (Go modules)
install:
	@echo "Installing dependencies..."
	@$(GO) mod tidy  # Ensure modules are tidy
	@$(GO) get $(DEPENDENCIES)  # Install listed dependencies

# Build target (build both cdrcfg and cdrgen)
build: build-cdrcfg build-cdrgen

# Build cdrcfg
build-cdrcfg:
	@echo "Building cdrcfg..."
	@mkdir -p $(BIN)
	@$(GOBUILD) -o $(CDRCFG) -ldflags "-X main.version=$(VERSION)" $(SRC_CDRCFG)

# Build cdrgen
build-cdrgen:
	@echo "Building cdrgen..."
	@mkdir -p $(BIN)
	@$(GOBUILD) -o $(CDRGEN) -ldflags "-X main.version=$(VERSION)" $(SRC_CDRGEN)

# Clean up the binaries and binary directory
clean:
	@echo "Cleaning up..."
	@$(GOCLEAN)
	rm -f $(CDRCFG) $(CDRGEN)
	rm -rf $(BIN)

# Run cdrcfg
run-cdrcfg: build-cdrcfg
	@echo "Running cdrcfg..."
	@$(CDRCFG)

# Run cdrgen
run-cdrgen: build-cdrgen
	@echo "Running cdrgen..."
	@$(CDRGEN)

# Test the application
test:
	@echo "Running tests..."
	@$(GOTEST) -v ./...

# Format the Go code
format:
	@echo "Formatting Go code..."
	@$(GOFMT) ./...

# Run Go vet to analyze code
vet:
	@echo "Running Go vet..."
	@$(GOVET) ./...

# Build and run the Docker image
docker:
	@echo "Building Docker image..."
	docker build -t cdrcfg-cdrgen .

# Install dependencies, build, and test the application
install_and_test: install test build

# run all 
run: run-cdrcfg run-cdrgen 