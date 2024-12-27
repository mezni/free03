package main

import (
	"fmt"
	"log"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
)

func main() {
	// Initialize repository for NetworkTechnology
	dbPath := "./mydb.db"
	networkTechRepo, err := boltstore.NewNetworkTechnologyRepository(dbPath, "network_technologies")
	if err != nil {
		log.Fatalf("Failed to create network technology repository: %v", err)
	}

	// Get max ID once for network technologies
	maxID, err := networkTechRepo.GetMaxID()
	if err != nil {
		log.Fatalf("Error getting max ID: %v", err)
	}

	// List of map data for network technologies
	networkTechnologiesMaps := []map[string]interface{}{
		{
			"Name":        "5G",
			"Description": "Fifth generation of mobile networks",
		},
		{
			"Name":        "Wi-Fi",
			"Description": "Wireless networking technology",
		},
		{
			"Name":        "4G",
			"Description": "Fourth generation of mobile networks",
		},
	}

	// Create a slice of NetworkTechnology entities
	var networkTechnologies []entities.NetworkTechnology
	for i, techMap := range networkTechnologiesMaps {
		name, ok := techMap["Name"].(string)
		if !ok || name == "" {
			// Skip invalid or empty Name
			continue
		}

		description, _ := techMap["Description"].(string)

		// Create the NetworkTechnology entity with maxID + 1 + i (to get a unique ID)
		networkTech := entities.NetworkTechnology{
			ID:          maxID + 1 + i,  // Assign unique ID based on maxID
			Name:        name,
			Description: description,
		}

		// Call Create to insert or skip if exists
		createdTech, err := networkTechRepo.Create(networkTech)
		if err != nil {
			log.Fatalf("Error creating network technology: %v", err)
		}

		// Append the created or existing technology to the slice
		networkTechnologies = append(networkTechnologies, createdTech)
	}

	// Display the created technologies
	fmt.Println("Created Network Technologies:")
	for _, tech := range networkTechnologies {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", tech.ID, tech.Name, tech.Description)
	}
	networkTechRepo.Close()

	// Initialize repository for NetworkElementType
	networkElementTypeRepo, err := boltstore.NewNetworkElementTypeRepository(dbPath, "network_element_types")
	if err != nil {
		log.Fatalf("Error initializing NetworkElementType repository: %v", err)
	}
	
	// Create and insert NetworkElementTypes
	networkElementTypesMaps := []map[string]interface{}{
		{
			"Name":                  "Router",
			"Description":           "Device that forwards data packets between networks",
			"NetworkTechnologyName": "5G",
		},
		{
			"Name":                  "Access Point",
			"Description":           "Device that allows wireless devices to connect to a wired network",
			"NetworkTechnologyName": "Wi-Fi",
		},
	}

	// Create a slice of NetworkElementType entities
	var networkElementTypes []entities.NetworkElementType
	for _, elemMap := range networkElementTypesMaps {
		name, ok := elemMap["Name"].(string)
		if !ok || name == "" {
			continue
		}

		description, _ := elemMap["Description"].(string)
		networkTechnologyName, _ := elemMap["NetworkTechnologyName"].(string)

		// Create a new NetworkElementType with unique ID
		networkElemType := entities.NetworkElementType{
			Name:                  name,
			Description:           description,
			NetworkTechnologyName: networkTechnologyName,
		}

		// Call Create to insert or skip if exists
		createdElem, err := networkElementTypeRepo.Create(networkElemType)
		if err != nil {
			continue
		}

		networkElementTypes = append(networkElementTypes, createdElem)
	}

	// Display the created network element types
	fmt.Println("Created Network Element Types:")
	for _, elem := range networkElementTypes {
		fmt.Printf("ID: %d, Name: %s, Description: %s, NetworkTechnologyName: %s\n", elem.ID, elem.Name, elem.Description, elem.NetworkTechnologyName)
	}

	// Retrieve and print all network element types
	elementTypes, err := networkElementTypeRepo.FindAll()
	if err != nil {
		log.Fatalf("Error finding all network element types: %v", err)
	}

	fmt.Println("\nAll Network Element Types in DB:")
	for _, elem := range elementTypes {
		fmt.Printf("ID: %d, Name: %s, Description: %s, NetworkTechnologyName: %s\n", elem.ID, elem.Name, elem.Description, elem.NetworkTechnologyName)
	}

	// Close the NetworkElementType repository
	networkElementTypeRepo.Close()
}
