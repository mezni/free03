package main

import (
	"log"
	"strconv"
	"time"

	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

func main() {
	// Initialize BoltDB manager
	manager, err := boltstore.NewBoltDBManager[entities.NetworkTechnology]("example.db", 5*time.Second)
	if err != nil {
		log.Fatalf("Failed to initialize BoltDBManager: %v", err)
	}
	defer manager.Close()

	// Define a list of NetworkTechnology entities
	networkTechnologies := []entities.NetworkTechnology{
		{Name: "5G", Description: "Fifth-generation mobile network"},
		{Name: "4G", Description: "Fourth-generation mobile network"},
		{Name: "5G", Description: "Duplicate Name (should be skipped)"},
	}

	// Get the maximum ID from the "network_tech_bucket" and calculate the next ID
	maxID, err := manager.GetMaxID("network_tech_bucket", func(item entities.NetworkTechnology) int {
		return item.ID
	})
	if err != nil {
		log.Fatalf("Failed to get max ID: %v", err)
	}

	// Now load the list into the "network_tech_bucket"
	for i, item := range networkTechnologies {
		// Set the ID of the new item to maxID + 1
		item.ID = maxID + i + 1

		// Define the columns to check for duplicates (e.g., Name)
		columnsToCheck := []string{"Name"}

		// Load the item into the database and check for duplicates
		err = manager.LoadList("network_tech_bucket", []entities.NetworkTechnology{item}, func(item entities.NetworkTechnology) string {
			return strconv.Itoa(item.ID) // Use ID as the key (converted to string)
		}, columnsToCheck, func(item entities.NetworkTechnology) int {
			return item.ID // Use ID as the identifying property
		})
		if err != nil {
			log.Fatalf("Failed to load network technology: %v", err)
		}
	}

	// Dump the list from the "network_tech_bucket"
	dumpedNt, err := manager.DumpList("network_tech_bucket")
	if err != nil {
		log.Fatalf("Failed to dump network technologies: %v", err)
	}
	log.Printf("Dumped Network Technologies: %+v\n", dumpedNt)
}
