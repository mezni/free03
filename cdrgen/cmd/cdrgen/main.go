package main

import (
	"github.com/mezni/wovoka/cdrgen/application/services"
	"log"
)

func main() {

	// Initialize the service with the config file
	service, err := services.NewInitCacheService()
	if err != nil {
		log.Fatalf("Error initializing service: %v", err)
	}

	// Initialize the database using the service
	if err := service.InitCache(); err != nil {
		log.Fatalf("Error initializing database: %v", err)
	}
}
