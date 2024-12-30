package main

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
)

func main() {
	// Step 1: Define the BoltDB configuration
	config := boltstore.BoltDBConfig{
		DBName:     "example.db",
		BucketName: "network_technologies",
	}

	// Step 2: Prepare data to save (NetworkTechnology instances)
	networkTechnologies := []*entities.NetworkTechnology{
		{ID: 1, Name: "5G", Description: "Fifth Generation Mobile Network"},
		{ID: 2, Name: "Wi-Fi 6", Description: "Latest Wi-Fi standard"},
		{ID: 3, Name: "LTE", Description: "4G mobile network technology"},
	}

	// Convert NetworkTechnology structs to maps
	var data []map[string]interface{}
	for _, nt := range networkTechnologies {
		data = append(data, nt.ToMap())
	}

	// Step 3: Save data to BoltDB
	fmt.Println("Saving data to BoltDB...")
	err := boltstore.SaveToBoltDB(config, data)
	if err != nil {
		log.Fatalf("Error saving to BoltDB: %v", err)
	} else {
		fmt.Println("Data saved successfully.")
	}

}
