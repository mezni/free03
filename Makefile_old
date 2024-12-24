GO            = go
GOBUILD       = $(GO) build
GOCLEAN       = $(GO) clean
GOTEST        = $(GO) test
GOGET         = $(GO) get
GOFMT         = $(GO) fmt
GOVET         = $(GO) vet

BINARY        = wovoka
SRC           = configurator/cmd/main.go
BIN           = bin

DEPENDENCIES  = github.com/boltdb/bolt github.com/stretchr/testify/assert

# Default target
all: install build

# Install dependencies (Go modules)
install:
	@echo "Installing dependencies..."
	@$(GO) mod tidy  # Ensure modules are tidy
	@$(GO) get $(DEPENDENCIES)  # Install listed dependencies

# Build the application
build:
	@echo "Building the application..."
	@$(GOBUILD) -o $(BIN)/$(BINARY) $(SRC)

# Clean up the binary and binary directory
clean:
	@echo "Cleaning up..."
	@$(GOCLEAN)
	rm -f $(BIN)/$(BINARY)
	rm -rf $(BIN)

# Run the application
run: build
	@echo "Running the application..."
	@$(GO) run $(SRC)

# Test the application
test:
	@echo "Running tests..."
	@$(GOTEST) -v ./...

# Format the Go code
format:
	@echo "Formatting Go code..."
	@go fmt ./...

# Run Go vet to analyze code
vet:
	@echo "Running Go vet..."
	@$(GOVET) ./...

# Build and run the Docker image
docker:
	@echo "Building Docker image..."
	docker build -t $(BINARY) .

# Install dependencies, build, and test the application
install_and_test: install test
