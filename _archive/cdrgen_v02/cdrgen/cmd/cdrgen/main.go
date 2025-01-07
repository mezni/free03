package main

import (
	"log"

	"github.com/mezni/wovoka/cdrgen/application/services"
)

const (
	dbFile = "./cdrgen.db"
)

func main() {
	// Initialize the CdrGeneratorService
	cdrGeneratorService, err := services.NewCdrGeneratorService(dbFile)
	if err != nil {
		log.Fatalf("Error initializing CdrGeneratorService: %v", err)
	}
	defer func() {
		if err := cdrGeneratorService.DB.Close(); err != nil {
			log.Printf("Error closing database connection: %v", err)
		}
	}()

	// Generate the data
	if err := cdrGeneratorService.Generate(); err != nil {
		log.Fatalf("Error during data generation: %v", err)
	}

	log.Println("Data generation process completed successfully.")
}
