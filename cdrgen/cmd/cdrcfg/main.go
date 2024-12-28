package main

import (
	"github.com/boltdb/bolt"
	"github.com/mezni/wovoka/cdrgen/application/services"
	"log"
)

func main() {
	// Open BoltDB file
	db, err := bolt.Open("network_data.db", 0600, nil)
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Create BaselineLoaderService
	loaderService := &services.BaselineLoaderService{DB: db}

	// Load baseline data from JSON file
	err = loaderService.LoadData("baseline.json")
	if err != nil {
		log.Fatal(err)
	}

	log.Println("Data loaded and saved successfully!")
}
