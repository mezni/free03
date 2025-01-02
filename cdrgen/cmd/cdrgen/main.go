package main

import (
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
	"github.com/mezni/wovoka/cdrgen/application/services"
	"database/sql"
	"fmt"
	"log"
	_ "github.com/mattn/go-sqlite3"
)

func main() {
	// Initialize SQLite database
	db, err := sql.Open("sqlite3", "./config.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Initialize repositories
	networkTechnologyRepo := sqlitestore.NewNetworkTechnologyRepository(db)

	// Create necessary tables in the database
	if err := networkTechnologyRepo.CreateTables(); err != nil {
		log.Fatalf("Error creating tables: %v", err)
	}

	// Initialize ApplicationService
	configLoaderService := services.NewConfigLoaderService(networkTechnologyRepo)

	// Load data from JSON and save to database
	if err := configLoaderService.LoadAndSaveData("data/baseline.json"); err != nil {
		log.Fatalf("Error processing data: %v", err)
	}

	fmt.Println("Data loaded and saved successfully!")
}
