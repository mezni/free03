package main

import (
	"fmt"
	"github.com/mezni/wovoka/configurator/domain/entities"
	"github.com/mezni/wovoka/configurator/infrastructure/persistance/boltstore"
	"log"
)

func main() {
	// Define the path to your BoltDB file
	dbFile := "locations.db"

	// Initialize the BoltDB location repository
	repo, err := boltstore.NewBoltDBLocationRepository(dbFile)
	if err != nil {
		log.Fatalf("Error initializing repository: %v", err)
	}
	defer repo.Close()

	// Create a new location
	location, err := entities.NewLocation(101, entities.NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	if err != nil {
		log.Fatalf("Error creating location: %v", err)
	}

	// Add location to the repository
	err = repo.Create(location)
	if err != nil {
		log.Fatalf("Error adding location to repository: %v", err)
	}

	// Get location by ID
	retrievedLocation, err := repo.GetByID(101)
	if err != nil {
		log.Fatalf("Error retrieving location by ID: %v", err)
	}
	fmt.Printf("Retrieved Location: %+v\n", retrievedLocation)

	// Update the location
	location.LocationName = "Uptown"
	err = repo.Update(location)
	if err != nil {
		log.Fatalf("Error updating location: %v", err)
	}

	// Get all locations
	allLocations, err := repo.GetAll()
	if err != nil {
		log.Fatalf("Error retrieving all locations: %v", err)
	}
	fmt.Println("All Locations:")
	for _, loc := range allLocations {
		fmt.Printf("%+v\n", loc)
	}

	// Delete the location
	err = repo.Delete(101)
	if err != nil {
		log.Fatalf("Error deleting location: %v", err)
	}

	// Try to retrieve the deleted location
	_, err = repo.GetByID(101)
	if err != nil {
		fmt.Printf("Expected error after deletion: %v\n", err)
	}
}
