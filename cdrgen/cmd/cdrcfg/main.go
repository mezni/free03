package main

import (
	"log"
	"github.com/mezni/wovoka/cdrgen/sqlitestore"
	"github.com/mezni/wovoka/cdrgen/repositories"
	"github.com/mezni/wovoka/cdrgen/services"
)

func main() {
	// Initialize SQLite repository
	sqliteRepo := sqlitestore.NewBaselineSQLiteRepository()
	err := sqliteRepo.Open("baseline.db")
	if err != nil {
		log.Fatalf("Failed to open database: %v", err)
	}
	defer sqliteRepo.Close()

	// Create tables if not exist
	err = sqliteRepo.CreateTables()
	if err != nil {
		log.Fatalf("Failed to create tables: %v", err)
	}

	// Create service
	service := services.NewBaselineService(
		sqliteRepo, // Inject the repository into the service
		sqliteRepo,
		sqliteRepo,
	)

	// Example: Insert a network technology
	err = service.InsertNetworkTechnology("5G", "Fifth generation mobile network technology")
	if err != nil {
		log.Printf("Failed to insert network technology: %v", err)
	}

	// Example: Get all network technologies
	technologies, err := service.GetAllNetworkTechnologies()
	if err != nil {
		log.Printf("Failed to retrieve network technologies: %v", err)
	} else {
		log.Printf("Network Technologies: %+v", technologies)
	}
}
