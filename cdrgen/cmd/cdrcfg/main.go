package main

import (
	"fmt"
	"log"
	"github.com/mezni/wovoka/cdrgen/application/services"
)

func main() {
	// Path to your JSON file
	filePath := "baseline.json"


	// Initialize the BaselineService
	service := services.NewBaselineService(filePath)

	// Map the DTOs to entities
	networkTechnologies, networkElementTypes, serviceTypes, err := service.MapFileDataToEntities()
	if err != nil {
		log.Fatalf("Error mapping file data to entities: %v", err)
	}

	// Print the mapped NetworkTechnologies
	fmt.Println("Network Technologies:")
	for _, nt := range networkTechnologies {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", nt.ID, nt.Name, nt.Description)
	}

	// Print the mapped NetworkElementTypes
	fmt.Println("\nNetwork Element Types:")
	for _, netElem := range networkElementTypes {
		fmt.Printf("ID: %d, Name: %s, Description: %s, NetworkTechnology: %s\n", 
			netElem.ID, netElem.Name, netElem.Description, netElem.NetworkTechnology)
	}

	// Print the mapped ServiceTypes
	fmt.Println("\nService Types:")
	for _, service := range serviceTypes {
		fmt.Printf("ID: %d, Name: %s, Description: %s, NetworkTechnology: %s\n", 
			service.ID, service.Name, service.Description, service.NetworkTechnology)
	}
}
