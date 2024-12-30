package services

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore"
)

type BaselineDumperService struct {
	dbFile string
}

func NewBaselineDumperService(dbFile string) *BaselineDumperService {
	return &BaselineDumperService{
		dbFile: dbFile,
	}
}

// DumpBaseline dumps the data from the specified BoltDB buckets into an in-memory repository and optionally outputs it.
func (ls *BaselineDumperService) DumpBaseline() error {
	// Read data from the "network_technologies" bucket
	networkTechnologies, err := boltstore.ReadFromBoltDB(ls.dbFile, networkTechnologiesBucket)
	if err != nil {
		return fmt.Errorf("error reading network technologies from DB: %w", err)
	}

	// Initialize the in-memory repository
	networkTechnologyRepo := inmemstore.NewInMemoryNetworkTechnologyRepository()

	// Iterate over the fetched data and save it to the in-memory repository
	for _, ntData := range networkTechnologies {
		// Convert the generic interface{} to the appropriate type (e.g., NetworkTechnology)
		ntMap, ok := ntData.(map[string]interface{})
		if !ok {
			return fmt.Errorf("failed to convert network technology data: %v", ntData)
		}

		// Create a NetworkTechnology entity
		networkTechnology := &entities.NetworkTechnology{
			ID:          int(ntMap["ID"].(float64)), // Convert float64 to int
			Name:        ntMap["Name"].(string),
			Description: ntMap["Description"].(string),
		}

		// Save the entity to the repository
		err := networkTechnologyRepo.Save(networkTechnology)
		if err != nil {
			return fmt.Errorf("error saving network technology to repository: %w", err)
		}
	}

	fmt.Println("Data dump completed successfully.")
	return nil
}
