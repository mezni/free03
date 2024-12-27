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
	defer networkTechRepo.Close()  // Corrected: Calling Close() without expecting a value

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

	// Retrieve and print all network technologies
	technologies, err := networkTechRepo.FindAll()
	if err != nil {
		log.Fatalf("Error finding all network technologies: %v", err)
	}

	fmt.Println("\nAll Network Technologies in DB:")
	for _, tech := range technologies {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", tech.ID, tech.Name, tech.Description)
	}
}
