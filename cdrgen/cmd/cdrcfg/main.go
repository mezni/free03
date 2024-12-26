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
		{ID: 1, Name: "5G", Description: "Fifth-generation mobile network"},
		{ID: 2, Name: "4G", Description: "Fourth-generation mobile network"},
	}

	// Load the list into the "network_tech_bucket"
	err = manager.LoadList("network_tech_bucket", networkTechnologies, func(item entities.NetworkTechnology) string {
		return strconv.Itoa(item.ID) // Use ID as the key (converted to string)
	})
	if err != nil {
		log.Fatalf("Failed to load network technologies: %v", err)
	}

	// Dump the list from the "network_tech_bucket"
	dumpedNt, err := manager.DumpList("network_tech_bucket")
	if err != nil {
		log.Fatalf("Failed to dump network technologies: %v", err)
	}
	log.Printf("Dumped Network Technologies: %+v\n", dumpedNt)
}