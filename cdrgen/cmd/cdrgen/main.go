package main

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore"
)

func main() {
	config := boltstore.BoltDBConfig{
		DBName:     "example.db",
		BucketName: "network_technologies",
	}
	repo := inmemstore.NewNetworkTechnologyRepositoryInMemory()

	// Step 4: Read data from BoltDB
	fmt.Println("Reading data from BoltDB...")
	entitiesMap, err := boltstore.ReadFromBoltDB(config)
	if err != nil {
		log.Fatalf("Error reading from BoltDB: %v", err)
	} else {
		// Convert map back to NetworkTechnology structs
		for _, item := range entitiesMap {
			nt, err := entities.FromMap(item)
			if err != nil {
				log.Printf("Error converting map to NetworkTechnology: %v", err)
				continue
			}
			repo.Save(nt)
		}
	}

	technologies, _ := repo.FindAll()
	for _, tech := range technologies {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", tech.ID, tech.Name, tech.Description)
	}
}
