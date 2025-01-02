package main

import (
	"database/sql"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
	"github.com/mezni/wovoka/cdrgen/application/services"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
	"log"
)

func main() {
	// Initialize SQLite database
	db, err := sql.Open("sqlite3", "./config.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Initialize repositories
	networkTechnologyRepo, err := sqlitestore.NewNetworkTechnologyRepository("./config.db")
	if err != nil {
		log.Fatal(err)
	}

	// Initialize ApplicationService
	configLoaderService := services.NewConfigLoaderService(*networkTechnologyRepo)

	// Load data from JSON and save to database
	if err := configLoaderService.LoadAndSaveData("data/baseline.json"); err != nil {
		log.Fatalf("Error processing data: %v", err)
	}

	fmt.Println("Data loaded and saved successfully!")
}
