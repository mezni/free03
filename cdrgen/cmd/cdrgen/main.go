package main

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/application/services"
)

func main() {
	// Initialize the loader service
	loaderService, err := services.NewLoaderService("cdrgen.db")
	if err != nil {
		log.Fatalf("Error initializing loader service: %v", err)
	}
	defer loaderService.Close()

	// Step 1: Retrieve all network technologies from the database
	networkTechnologies, err := loaderService.NetworkTechRepo.GetAll()
	if err != nil {
		log.Fatalf("Error retrieving network technologies: %v", err)
	}

	// Step 2: Print the retrieved network technologies
	fmt.Println("All Network Technologies in Database:")
	for _, nt := range networkTechnologies {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", nt.ID, nt.Name, nt.Description)
	}
}
