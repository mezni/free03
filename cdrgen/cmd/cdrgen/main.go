package main

import (
	"fmt"
	"log"

//	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
)

func main() {
	// Step 1: Define the BoltDB configuration
	config := boltstore.BoltDBConfig{
		DBName:     "example.db",
		BucketName: "network_technologies",
	}

	// Initialize in-memory repository
	repo := inmemstore.NewNetworkTechnologyRepositoryInMemory()

	// Step 2: Read data from BoltDB
	fmt.Println("Reading data from BoltDB...")
	entitiesMap, err := boltstore.ReadFromBoltDB(config)
	if err != nil {
		log.Fatalf("Error reading from BoltDB: %v", err)
	}

	// Initialize the NetworkTechnologyMapper
	ntMapper := &mappers.NetworkTechnologyMapper{}

	// Step 3: Convert maps to NetworkTechnology structs using FromListMap
	networkTechnologies, err := ntMapper.FromListMap(entitiesMap)
	if err != nil {
		log.Fatalf("Error converting from map to NetworkTechnology: %v", err)
	}

	// Step 4: Save data to in-memory repository
	for _, nt := range networkTechnologies {
		err := repo.Save(nt)
		if err != nil {
			log.Printf("Error saving to in-memory repository: %v", err)
		}
	}

	// Step 5: Retrieve and display saved technologies
	technologies, _ := repo.FindAll()
	for _, tech := range technologies {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", tech.ID, tech.Name, tech.Description)
	}
}
