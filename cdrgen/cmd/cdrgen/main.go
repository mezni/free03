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

	// Step 3: Retrieve all network element types from the database
	networkElementTypes, err := loaderService.NetworkElementTypeRepo.GetAll()
	if err != nil {
		log.Fatalf("Error retrieving network element types: %v", err)
	}

	// Step 4: Print the retrieved network element types
	fmt.Println("\nAll Network Element Types in Database:")
	for _, net := range networkElementTypes {
		fmt.Printf("ID: %d, Name: %s, Description: %s, Network Technology: %s\n",
			net.ID, net.Name, net.Description, net.NetworkTechnology)
	}
}
