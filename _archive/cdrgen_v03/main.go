package main

import (
	"fmt"
	"log"
	"time"

	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

func main() {
	// Initialize the database manager
	manager, err := boltstore.NewBoltDBManager("data.db", 5*time.Second)
	if err != nil {
		log.Fatal("Failed to initialize BoltDB:", err)
	}
	defer manager.Close()

	// Initialize the example repository
	configRepo := boltstore.NewConfigRepository(manager)

	// Convert PredefinedNetworkTechnologies to map[string]interface{}
	items := make(map[string]interface{})
	for key, tech := range entities.PredefinedNetworkTechnologies {
		items[key] = tech
	}

	// Save predefined network technologies to the database
	if err := configRepo.SaveMany("NetworkTechnologies", items); err != nil {
		log.Fatal("Failed to save network technologies:", err)
	}

	// Retrieve all network technologies from the "NetworkTechnologies" bucket
	var allData []entities.NetworkTechnology
	if err := configRepo.GetAll("NetworkTechnologies", &allData); err != nil {
		log.Fatal("Failed to retrieve all data:", err)
	}

	// Print all retrieved data
	fmt.Println("All Network Technologies:")
	for _, data := range allData {
		fmt.Printf("ID: %s, Name: %s, Description: %s\n", data.ID, data.Name, data.Description)
	}
}
