package main

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/application/services"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore"
)

const (
	configFile = "config.yaml"
	dbName     = "cdrcfg.db"
)

func main() {
	fmt.Println("Starting application...")

	// Initialize the LoaderService with the config file and database name
	loaderService := services.NewLoaderService(configFile, dbName)

	// Call DumpLocations to read and return locations
	locations, err := loaderService.DumpLocations()
	if err != nil {
		log.Fatalf("Error dumping locations: %v", err)
	}

	// Initialize the in-memory repository
	repo := inmemstore.NewInMemoryLocationRepository()

	// Add dumped locations to the repository
	for _, loc := range locations {
		err := repo.Create(&entities.Location{
			ID:             loc.ID,
			Name:             loc.Name,
			NetworkTechnology: loc.NetworkTechnology,
			LatitudeMin: loc.LatitudeMin,
			LatitudeMax: loc.LatitudeMax,
			LongitudeMin: loc.LongitudeMin,
			LongitudeMax: loc.LongitudeMax,
			AreaCode: loc.AreaCode,
		})
		if err != nil {
			log.Fatalf("Error creating location: %v", err)
		}
	}

	// Retrieve and print all locations from the repository
	allLocations, err := repo.GetAll()
	if err != nil {
		log.Fatalf("Error retrieving locations from repository: %v", err)
	}

	fmt.Printf("Loaded %d locations into the repository:\n", len(allLocations))
	for _, loc := range allLocations {
		fmt.Printf("ID: %d, Name: %s, NetworkTechnology: %s\n", loc.ID, loc.Name, loc.NetworkTechnology)
	}
}
