package main

import (
	"log"
	//	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
	//	"github.com/mezni/wovoka/cdrgen/repositories"
	"github.com/mezni/wovoka/cdrgen/application/services"
	// "github.com/mezni/wovoka/cdrgen/domain/entities"
)

const (
	dbFile       = "baseline.db"
	jsonFilename = "data/baseline.json"
)

func main() {
	log.Printf("Startup")
	// Initialize the LoaderService
	loader, err := services.NewLoaderService(dbFile)
	if err != nil {
		log.Fatalf("Failed to initialize loader service: %v", err)
	}
	defer func() {
		if err := loader.Close(); err != nil {
			log.Printf("Error closing loader service: %v", err)
		}
	}()

	// Load and save data from the JSON file
	if err := loader.LoadAndSaveBaseline(jsonFilename); err != nil {
		log.Fatalf("Error loading and saving data: %v", err)
	}

	log.Println("Application completed successfully.")
}
