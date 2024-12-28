package main

import (
	"log"

	"go.etcd.io/bbolt"
	"github.com/mezni/wovoka/cdrgen/application/services"
)

func main() {
	// Open the bbolt database file
	db, err := bbolt.Open("network_data.db", 0600, nil)
	if err != nil {
		log.Fatalf("error opening database: %v", err)
	}
	defer func() {
		if err := db.Close(); err != nil {
			log.Fatalf("error closing database: %v", err)
		}
	}()

	// Create and use BaselineLoaderService
//	baselineLoader := &services.BaselineLoaderService{DB: db}
//	if err := baselineLoader.LoadData("baseline.json"); err != nil {
//		log.Fatalf("error loading baseline data: %v", err)
//	}
//	log.Println("Baseline data loaded and saved successfully!")

	// Create and use BusinessLoaderService
	businessLoader := &services.BusinessLoaderService{DB: db}
	if err := businessLoader.LoadData("config.yaml"); err != nil {
		log.Fatalf("error loading business data: %v", err)
	}
	log.Println("Business data loaded and saved successfully!")
}
