package main

import (
	"context"
	"fmt"
	"github.com/google/uuid"
	"github.com/mezni/wovoka/cdrgen/internal/infrastructure/logger"
	"github.com/mezni/wovoka/cdrgen/internal/infrastructure/yamlreader"
	"os"
	"strings"
)

func main() {
	// Create a logger instance using the correct alias 'logger'
	l := logger.NewSimpleLogger(os.Stdout, logger.DebugLevel)

	// Generate a unique request ID
	requestID := uuid.New().String()

	// Split the requestID by the '-' and take the first part
	requestID = strings.Split(requestID, "-")[0]

	// Create context with module and request_id information
	ctx := context.WithValue(context.Background(), "module", "cdrcfg")
	ctx = context.WithValue(ctx, "context", requestID)

	// Log the startup message
	l.Info(ctx, "Startup")

	// Declare a variable to store the YAML data
	var data map[string]interface{}

	// Read the YAML file into the `data` map
	err := yamlreader.ReadYAML("config.yaml", &data)
	if err != nil {
		// Log the error and exit if reading YAML fails
		l.Error(ctx, fmt.Sprintf("Error reading YAML: %v", err))
		return
	}

	// Ensure 'locations' exists and is a slice of interfaces
	locations, ok := data["locations"].([]interface{})
	if !ok {
		l.Error(ctx, "Error: locations field is missing or not a list")
		return
	}

	// Iterate over the locations and print each one
	for _, location := range locations {
		loc, ok := location.(map[string]interface{})
		if !ok {
			l.Error(ctx, "Error: location is not a valid map")
			continue
		}
		// Print Location ID and Name
		fmt.Printf("Location ID: %v, Name: %v\n", loc["id"], loc["name"])
	}

	// Log the shutdown message
	l.Info(ctx, "Shutdown")
}
