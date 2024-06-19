BINARY_NAME=reader.exe

build:
	go build -o ./reader/bin/${BINARY_NAME} ./reader/main.go

run: build
	./${BINARY_NAME}
	
clean:
	go clean
#	rm ${BINARY_NAME}

test:
	go test ./...

test_coverage:
	go test ./... -coverprofile=coverage.out

dep:
	go mod download

vet:
	go vet

lint:
	golangci-lint run --enable-all