package main

import (
	"fmt"
	"log"
	"github.com/mezni/wovoka/cdrgen/application/services"
//	"github.com/mezni/wovoka/cdrgen/application/mappers" 
)


func main() {
	configFile := "baseline.json"
	dbFile := "database.db"

	loaderService := services.NewBaselineLoaderService(configFile, dbFile)

	// Load and process the baseline
	err := loaderService.LoadBaseline()
	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	fmt.Println("Baseline loading complete.")
}