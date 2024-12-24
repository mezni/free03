package main

import (
	"fmt"
	"github.com/mezni/wovoka/domain/services"
	"github.com/mezni/wovoka/internal/persistance"
	"log"
)

func main() {
	// Create an in-memory repository
	repo := persistance.NewInMemoryServiceRepository()

	// Create a new ServiceService
	serviceService := services.NewServiceService(repo)

	// Load and store services from services.json in /configs folder
	err := serviceService.LoadAndStoreServices("configs/services.json")
	if err != nil {
		log.Fatalf("Error loading and storing services: %v", err)
	}

	// List services from the repository
	allServices, err := serviceService.ListServices()
	if err != nil {
		log.Fatalf("Error listing services: %v", err)
	}

	fmt.Println("Services in repository:")
	for _, service := range allServices {
		fmt.Printf("%+v\n", service)
	}
}
