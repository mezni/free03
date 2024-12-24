package main

import (
	"fmt"
	"github.com/mezni/wovoka/configurator/domain/services"
	"github.com/mezni/wovoka/configurator/infrastructure/persistance/boltstore"
	"log"
)

func main() {
	dbPath := "mydb.db"
	// Example: Use an InMemory repository
	repo, _ := boltstore.NewBoltDBLocationRepository(dbPath)

	// Path to the configuration file (replace with your actual path)
	configFilePath := "configurator/configs/locations.json" // Ensure this file exists and is properly formatted

	// Initialize the LocationServiccd e with the config file and the repository
	service, err := services.NewLocationService(configFilePath, repo)
	if err != nil {
		log.Fatalf("Error initializing location service: %v", err)
	}

	// Generate locations based on the configuration and save them to the repository
	locations, err := service.GenerateLocations()
	if err != nil {
		log.Fatalf("Error generating locations: %v", err)
	}

	// Print the generated locations
	fmt.Println("Generated Locations:")
	for _, location := range locations {
		fmt.Printf("LocationID: %d, Name: %s, Latitude: %.2f-%.2f, Longitude: %.2f-%.2f\n",
			location.LocationID, location.LocationName, location.LatMin, location.LatMax, location.LonMin, location.LonMax)
	}

	// Optionally, retrieve a specific location by ID
	locationID := 101
	location, err := repo.GetByID(locationID)
	if err != nil {
		log.Printf("Error retrieving location with ID %d: %v", locationID, err)
	} else {
		fmt.Printf("\nRetrieved Location by ID %d: %v\n", locationID, location)
	}
}
