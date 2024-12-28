package main

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/infrastructure/yamlreader" 
)

func main() {
	// Initialize the ConfigReader
	configReader := yamlreader.NewConfigReader("config.yaml")

	// Read the configuration
	configData, err := configReader.Read()
	if err != nil {
		log.Fatalf("Error reading config: %v", err)
	}

	// Open BoltDB
	db, err := bbolt.Open("config.db", 0600, nil)
	if err != nil {
		log.Fatalf("Error opening BoltDB: %v", err)
	}
	defer db.Close()

	// Initialize repositories
	boltDBRepo := repositories.NewBoltDBLocationRepository(db)

	// Initialize LocationService with the configuration data
	locationService := services.NewLocationService(boltDBRepo, db, configData)

	// Load configuration from the provided map and save to BoltDB
	err = locationService.ToDB()
	if err != nil {
		log.Fatalf("Error loading config to BoltDB: %v", err)
	}

}
