GO            = go
GOBUILD       = $(GO) build
GOCLEAN       = $(GO) clean
GOTEST        = $(GO) test
GOGET         = $(GO) get
GOFMT         = $(GO)fmt
GOVET         = $(GO) vet

BINARY        = wovoka
#SRC           = $(shell find . -type f -name '*.go')
SRC           = cmd/main.go
BIN           = bin

all: build

build:
	$(GOBUILD) -o $(BIN)/$(BINARY) $(SRC)

clean:
	$(GOCLEAN)
	rm -f $(BIN)/$(BINARY)
	rm -rf $(BIN)

test:
	$(GOTEST) -v ./...

format:
	$(GOFMT) -w .

vet:
	$(GOVET) ./...

install:
	$(GOGET) ./...
	$(GO) install ./...

run:
	$(GO) run $(SRC)

docker:
	docker build -t $(BINARY) .