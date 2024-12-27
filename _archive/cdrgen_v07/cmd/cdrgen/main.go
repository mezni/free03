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
	networkTechnologyRepo, err := boltstore.NewNetworkTechnologyRepository(dbPath, "network_technologies")
	if err != nil {
		log.Fatalf("Failed to create network technology repository: %v", err)
	}
	defer networkTechnologyRepo.Close() // Close the DB connection when done

	// Get max ID once for network technologies
	maxID, err := networkTechnologyRepo.GetMaxID()
	if err != nil {
		log.Fatalf("Error getting max ID for network technologies: %v", err)
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
			// Handle invalid or empty Name
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
		createdTech, err := networkTechnologyRepo.Create(networkTech)
		if err != nil {
			log.Fatalf("Error creating network technology: %v", err)
		}

		// Append the created or existing technology to the slice
		networkTechnologies = append(networkTechnologies, createdTech)
	}

	// Display the created network technologies
	fmt.Println("Created Network Technologies:")
	for _, tech := range networkTechnologies {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", tech.ID, tech.Name, tech.Description)
	}

	// Retrieve and print all network technologies
	technologies, err := networkTechnologyRepo.FindAll()
	if err != nil {
		log.Fatalf("Error finding all network technologies: %v", err)
	}

	fmt.Println("\nAll Network Technologies in DB:")
	for _, tech := range technologies {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", tech.ID, tech.Name, tech.Description)
	}

	// Initialize repository for NetworkElementType
	networkElementTypeRepo, err := boltstore.NewNetworkElementTypeRepository(dbPath, "network_element_types")
	if err != nil {
		log.Fatalf("Failed to create network element type repository: %v", err)
	}
	defer networkElementTypeRepo.Close() // Close the DB connection when done

	// Get max ID once for network element types
	maxIDElementType, err := networkElementTypeRepo.GetMaxID()
	if err != nil {
		log.Fatalf("Error getting max ID for network element types: %v", err)
	}

	// List of map data for network element types
	networkElementTypesMaps := []map[string]interface{}{
		{
			"Name":        "Router",
			"Description": "Network device that forwards data packets between computer networks",
		},
		{
			"Name":        "Switch",
			"Description": "Device that connects devices on a computer network",
		},
		{
			"Name":        "Firewall",
			"Description": "Network security system that monitors and controls incoming and outgoing network traffic",
		},
	}

	// Create a slice of NetworkElementType entities
	var networkElementTypes []entities.NetworkElementType
	for i, elementMap := range networkElementTypesMaps {
		name, ok := elementMap["Name"].(string)
		if !ok || name == "" {
			// Handle invalid or empty Name
			continue
		}

		description, _ := elementMap["Description"].(string)

		// Create the NetworkElementType entity with maxID + 1 + i (to get a unique ID)
		networkElementType := entities.NetworkElementType{
			ID:          maxIDElementType + 1 + i,  // Assign unique ID based on maxID
			Name:        name,
			Description: description,
		}

		// Call Create to insert or skip if exists
		createdElement, err := networkElementTypeRepo.Create(networkElementType)
		if err != nil {
			log.Fatalf("Error creating network element type: %v", err)
		}

		// Append the created or existing element to the slice
		networkElementTypes = append(networkElementTypes, createdElement)
	}

	// Display the created network element types
	fmt.Println("\nCreated Network Element Types:")
	for _, element := range networkElementTypes {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", element.ID, element.Name, element.Description)
	}

	// Retrieve and print all network element types
	elementTypes, err := networkElementTypeRepo.FindAll()
	if err != nil {
		log.Fatalf("Error finding all network element types: %v", err)
	}

	fmt.Println("\nAll Network Element Types in DB:")
	for _, element := range elementTypes {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", element.ID, element.Name, element.Description)
	}
}
