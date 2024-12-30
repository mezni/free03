package main

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/application/services"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore"
	"log"
)

func main() {
	configFile := "baseline.json"
	dbFile := "database.db"

	// Initialize the BaselineLoaderService
	loaderService := services.NewBaselineLoaderService(configFile, dbFile)

	// Load and process the baseline
	err := loaderService.LoadBaseline()
	if err != nil {
		log.Fatalf("Error loading baseline: %v", err)
	}
	fmt.Println("Baseline loading complete.")

	// Initialize the BaselineDumperService
	dumperService := services.NewBaselineDumperService(dbFile)

	// Dump baseline data to the console
	err = dumperService.DumpBaseline() // Pass `true` to print data to console
	if err != nil {
		log.Fatalf("Error dumping baseline to console: %v", err)
	}

	// Create an in-memory repository
	networkTechnologyRepo := inmemstore.NewInMemoryNetworkTechnologyRepository()

	// Retrieve all data from the in-memory repository
	allData, err := networkTechnologyRepo.FindAll()
	if err != nil {
		log.Fatalf("Error retrieving data from repository: %v", err)
	}

	// Print the data from the in-memory repository
	fmt.Println("Dumped Network Technologies from In-Memory Repository:")
	for _, nt := range allData {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", nt.ID, nt.Name, nt.Description)
	}

	fmt.Println("All data dumps are complete.")
}
