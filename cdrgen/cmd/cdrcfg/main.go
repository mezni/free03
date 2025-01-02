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

	db, err := sql.Open("sqlite3", "./config.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	networkTechnologyRepo, err := sqlitestore.NewNetworkTechnologyRepository("./config.db")
	if err != nil {
		log.Fatal(err)
	}

	configLoaderService := services.NewConfigLoaderService(*networkTechnologyRepo)

	if err := configLoaderService.LoadAndSaveData("data/baseline.json"); err != nil {
		log.Fatalf("Error processing data: %v", err)
	}

	fmt.Println("Data loaded and saved successfully!")
}
