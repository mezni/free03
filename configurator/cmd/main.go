package main

import (
	"fmt"
	"log"
	"os"

	"github.com/mezni/wovoka/configurator/domain/entities"
	"github.com/mezni/wovoka/configurator/domain/repositories"
	"github.com/mezni/wovoka/configurator/inmemorystore"
	"github.com/mezni/wovoka/configurator/services"
)

func main() {
	// Get the path to the locations.json file
	configFilePath := "locations.json"

	// Initialize the repository (you can replace this with BoltDB if needed)
	repo := inmemorystore.NewInMemoryLocationRepository()

	// Create the LocationService with the repository and config file
	locationService, err := services.NewLocationService(configFilePath, repo)
	if err != nil {
		log.Fatalf("Error creating LocationService: %v", err)
	}

	// Generate locations based on the configuration in the JSON file
	locations, err := locationService.GenerateLocations()
	if err != nil {
		log.Fatalf("Error generating locations: %v", err)
	}

	// Print out the generated locations
	fmt.Println("Generated Locations:")
	for _, location := range locations {
		fmt.Printf("ID: %d, Name: %s, Network: %s, Lat: %.4f-%.4f, Lon: %.4f-%.4f\n",
			location.LocationID,
			location.LocationName,
			location.NetworkType,
			location.LatMin,
			location.LatMax,
			location.LonMin,
			location.LonMax,
		)
	}

	// Example: Fetching a random location by network type
	networkType := entities.NetworkType4G // or any other network type
	randomLocation, err := repo.GetRandomByNetworkType(networkType)
	if err != nil {
		log.Fatalf("Error fetching random location: %v", err)
	}

	fmt.Printf("\nRandom Location for Network Type %s: %v\n", networkType, randomLocation)
}
