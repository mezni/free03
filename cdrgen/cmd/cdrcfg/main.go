package main

import (
	"fmt"
	"log"
	"github.com/mezni/wovoka/cdrgen/infrastructure/config"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
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

	// Save generated locations to BoltDB
	err = boltstore.SaveToBoltDB("locations.db", "locations", []interface{}{locations})
	if err != nil {
		fmt.Println("Error saving to DB:", err)
		return
	}

	// Read the data back from the database
	data, err := boltstore.ReadFromBoltDB("locations.db", "locations")
	if err != nil {
		fmt.Println("Error reading from DB:", err)
		return
	}

	// Print the data read from the database
	for _, item := range data {
		fmt.Println(item)
	}
}
