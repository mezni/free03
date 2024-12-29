package main

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/application/services"
)

const (
	configFile = "config.yaml"
	dbName     = "cdrcfg.db"
)

func main() {
	fmt.Println("Starting application...")

	// Initialize the LoaderService with the config file and database name
	loaderService := services.NewLoaderService(configFile, dbName)

	// Call LoadLocations to load and save locations (no need to pass dbName)
	err := loaderService.LoadLocations()
	if err != nil {
		log.Println("Error loading locations:", err)
	} else {
		fmt.Println("Locations loaded and saved successfully.")
	}

	// Call DumpLocations to read and return locations
	locations, err := loaderService.DumpLocations()
	if err != nil {
		log.Fatalf("Error dumping locations: %v", err)
	}

	// Output the retrieved locations
	fmt.Printf("Dumped %d locations:\n", len(locations))
	for _, loc := range locations {
		fmt.Printf("Location: %+v\n", loc)
	}

}
