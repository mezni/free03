package main

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
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

	// Initialize the NetworkTechnologyMapper
	ntMapper := &mappers.NetworkTechnologyMapper{}

	// Step 3: Convert NetworkTechnology structs to maps using ToListMap
	data := ntMapper.ToListMap(networkTechnologies)

	// Step 4: Save data to BoltDB
	fmt.Println("Saving data to BoltDB...")
	err := boltstore.SaveToBoltDB(config, data)
	if err != nil {
		log.Fatalf("Error saving to BoltDB: %v", err)
	} else {
		fmt.Println("Data saved successfully.")
	}
}

