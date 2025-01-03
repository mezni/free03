

package main

import (
	"log"

	"github.com/mezni/wovoka/cdrgen/application/services"
)

const (
	dbFile       = "baseline.db"
	jsonFilename = "data/baseline.json"
	yamlFilename = "config.yaml"
)

func main() {
		log.Printf("Startup")
	loader, err := services.NewLoaderService(dbFile)
	if err != nil {
		log.Fatalf("Failed to initialize loader service: %v", err)
	}
	defer func() {
		if err := loader.Close(); err != nil {
			log.Printf("Error closing loader service: %v", err)
		}
	}()

	// Load and save baseline data
	if err := loader.LoadAndSaveBaseline(jsonFilename); err != nil {
		log.Fatalf("Error loading and saving baseline data: %v", err)
	}

	// Load and save business data
	if err := loader.LoadAndSaveBusiness(yamlFilename); err != nil {
		log.Fatalf("Error loading and saving business data: %v", err)
	}

	log.Println("Application completed successfully.")
}
