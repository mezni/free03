package main

import (
	"log"
//	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
//	"github.com/mezni/wovoka/cdrgen/repositories"
	"github.com/mezni/wovoka/cdrgen/application/services"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

func main() {
    log.Printf("Startup")

	// Initialize Loader Service
	loader, err := services.NewLoaderService("example.db")
	if err != nil {
		log.Fatalf("Failed to initialize LoaderService: %v", err)
	}
	defer loader.Close()

	// Setup the database (create tables)
	if err := loader.SetupDatabase(); err != nil {
		log.Fatalf("Failed to setup database: %v", err)
	}

	// Example usage: Insert and retrieve data using repositories
	networkTech := entities.NetworkTechnology{
		Name:        "4G LTE",
		Description: "Fourth generation mobile communication technology",
	}

	if err := loader.NetworkTechRepo.Insert(networkTech); err != nil {
		log.Fatalf("Failed to insert NetworkTechnology: %v", err)
	}

	networkTechnologies, err := loader.NetworkTechRepo.GetAll()
	if err != nil {
		log.Fatalf("Failed to retrieve NetworkTechnologies: %v", err)
	}

	log.Printf("Retrieved NetworkTechnologies: %+v\n", networkTechnologies)

	// Similarly, use NetworkElementTypeRepo and ServiceTypeRepo
}
