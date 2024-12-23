# Go parameters
GOCMD=go
GOBUILD=$(GOCMD) build
GOCLEAN=$(GOCMD) clean
GOTEST=$(GOCMD) test
GOGET=$(GOCMD) get
GOFMT=$(GOCMD) fmt
GOLINT=golint
GOVET=$(GOCMD) vet
BINARY_NAME=wovoka

# Build parameters
BUILD_DIR=./build
MAIN_GO_FILE=./main.go

# Test coverage parameters
TEST_COVERAGE_DIR=./test-coverage
TEST_COVERAGE_FILE=$(TEST_COVERAGE_DIR)/coverage.out

# Lint parameters
LINT_DIR=./lint
LINT_REPORT=$(LINT_DIR)/lint-report.txt

# Vet parameters
VET_DIR=./vet
VET_REPORT=$(VET_DIR)/vet-report.txt

# All target
all: format lint vet test build

# Build target
build:
	$(GOBUILD) -o $(BUILD_DIR)/$(BINARY_NAME) $(MAIN_GO_FILE)

# Test target
test:
	$(GOTEST) -v ./...

# Test coverage target
test_coverage:
	$(GOTEST) -coverprofile=$(TEST_COVERAGE_FILE) -covermode=atomic ./...
	$(GOCMD) tool cover -func=$(TEST_COVERAGE_FILE)

# Format target
format:
	$(GOFMT) -w -l .

# Lint target
lint:
	$(GOLINT) ./... > $(LINT_REPORT)

# Vet target
vet:
	$(GOVET) ./... > $(VET_REPORT)

# Clean target
clean:
	$(GOCLEAN)
	rm -f $(BUILD_DIR)/$(BINARY_NAME)
	rm -rf $(TEST_COVERAGE_DIR)
	rm -rf $(LINT_DIR)
	rm -rf $(VET_DIR)

# Run target
run:
	$(GOBUILD) -o $(BUILD_DIR)/$(BINARY_NAME) $(MAIN_GO_FILE)
	./$(BUILD_DIR)/$(BINARY_NAME)

# Get target
get:
	$(GOGET) -u

.PHONY: all build test test_coverage format lint vet clean run get
