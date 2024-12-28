package main

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/application/services"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

func main() {
	// Initialize services
	loaderService := &services.BaselineLoaderService{}
	dbService := &services.BoltPersistenceService{}

	// Open BoltDB
	if err := dbService.OpenDB("baseline.db"); err != nil {
		log.Fatalf("Error opening database: %v", err)
	}
	defer func() {
		if err := dbService.CloseDB(); err != nil {
			log.Printf("Error closing database: %v", err)
		}
	}()

	// Load baseline data
	result, err := loaderService.LoadData("baseline.json")
	if err != nil {
		log.Fatalf("Error loading data: %v", err)
	}

	// Access and save individual entity lists to BoltDB
	if err := dbService.SaveListToDB("NetworkTechnologies", result["NetworkTechnologies"].([]entities.NetworkTechnology), "all"); err != nil {
		log.Fatalf("Error saving NetworkTechnologies: %v", err)
	}
	if err := dbService.SaveListToDB("NetworkElementTypes", result["NetworkElementTypes"].([]entities.NetworkElementType), "all"); err != nil {
		log.Fatalf("Error saving NetworkElementTypes: %v", err)
	}
	if err := dbService.SaveListToDB("ServiceTypes", result["ServiceTypes"].([]entities.ServiceType), "all"); err != nil {
		log.Fatalf("Error saving ServiceTypes: %v", err)
	}

	fmt.Println("Data successfully loaded and saved to BoltDB.")
}
