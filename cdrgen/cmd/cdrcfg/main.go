package main

import (
	"github.com/mezni/wovoka/cdrgen/application/services"
	"log"
)

func main() {
	// Define the path for the config file
	configFile := "baseline.json"

	// Initialize the service with the config file
	service, err := services.NewInitDBService(configFile)
	if err != nil {
		log.Fatalf("Error initializing service: %v", err)
	}

	// Initialize the database using the service
	if err := service.InitDB(); err != nil {
		log.Fatalf("Error initializing database: %v", err)
	}
}
