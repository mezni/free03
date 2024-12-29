package main

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/infrastructure/config"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
)

const configFile = "config.yaml"

func main() {
	fmt.Println("Starting application...")

	// Load configuration
	cfg, err := config.LoadConfig(configFile)
	if err != nil {
		log.Fatalf("Failed to load configuration: %v", err)
	}

	// Initialize LocationService
	locationService := mappers.NewLocationService()

	// Generate locations
	locations, err := locationService.GenerateLocations(cfg)
	if err != nil {
		log.Fatalf("Error generating locations: %v", err)
	}

	// Output generated locations
	fmt.Printf("Generated %d locations:\n", len(locations))
	for _, loc := range locations {
		fmt.Printf("Location: %+v\n", loc)
	}
}
