package main

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/domain/services"
)

func main() {
	// Initialize repository for NetworkTechnology
	dbPath := "./mydb.db"
	networkTechRepo, err := boltstore.NewNetworkTechnologyRepository(dbPath, "network_technologies")
	if err != nil {
		log.Fatalf("Failed to create network technology repository: %v", err)
	}
	defer networkTechRepo.Close()

	// Initialize service for NetworkTechnology
	networkTechService := services.NewNetworkTechnologyService(networkTechRepo)

	// Create some sample NetworkTechnologies
	networkTechnologies := []entities.NetworkTechnology{
		{Name: "5G", Description: "Fifth generation of mobile networks"},
		{Name: "Wi-Fi", Description: "Wireless networking technology"},
		{Name: "4G", Description: "Fourth generation of mobile networks"},
	}

	// Insert the technologies into the repository
	createdTechnologies, err := networkTechService.CreateMany(networkTechnologies)
	if err != nil {
		log.Fatalf("Error creating network technologies: %v", err)
	}

	// Display the created technologies
	fmt.Println("Created Network Technologies:")
	for _, tech := range createdTechnologies {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", tech.ID, tech.Name, tech.Description)
	}

	// Retrieve and print all network technologies
	technologies, err := networkTechRepo.FindAll()
	if err != nil {
		log.Fatalf("Error finding all network technologies: %v", err)
	}

	fmt.Println("\nAll Network Technologies in DB:")
	for _, tech := range technologies {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", tech.ID, tech.Name, tech.Description)
	}

	// Optionally, get the maximum ID
	maxID, err := networkTechRepo.GetMaxID()
	if err != nil {
		log.Fatalf("Error getting max ID: %v", err)
	}
	fmt.Printf("\nThe current max ID is: %d\n", maxID)

	// Initialize repository for NetworkElementType
	networkElementTypeRepo, err := boltstore.NewNetworkElementTypeRepository(dbPath, "network_element_types")
	if err != nil {
		log.Fatalf("Failed to create network element type repository: %v", err)
	}
	defer networkElementTypeRepo.Close()

	// Initialize service for NetworkElementType
	networkElementTypeService := services.NewNetworkElementTypeService(networkElementTypeRepo)

	// Create sample NetworkElementTypes
	networkElementTypes := []entities.NetworkElementType{
		{Name: "Router", Description: "Network routing element", NetworkTechnologyName: "Wi-Fi"},
		{Name: "Switch", Description: "Network switching element", NetworkTechnologyName: "Ethernet"},
		{Name: "Gateway", Description: "Gateway between networks", NetworkTechnologyName: "5G"},
	}

	// Insert the NetworkElementTypes into the repository
	createdElements, err := networkElementTypeService.CreateMany(networkElementTypes)
	if err != nil {
		log.Fatalf("Error creating network element types: %v", err)
	}

	// Display the created NetworkElementTypes
	fmt.Println("\nCreated Network Element Types:")
	for _, element := range createdElements {
		fmt.Printf("ID: %d, Name: %s, Description: %s, Technology: %s\n", element.ID, element.Name, element.Description, element.NetworkTechnologyName)
	}

	// Retrieve and print all network element types
	elementTypes, err := networkElementTypeRepo.FindAll()
	if err != nil {
		log.Fatalf("Error finding all network element types: %v", err)
	}

	fmt.Println("\nAll Network Element Types in DB:")
	for _, element := range elementTypes {
		fmt.Printf("ID: %d, Name: %s, Description: %s, Technology: %s\n", element.ID, element.Name, element.Description, element.NetworkTechnologyName)
	}
}
