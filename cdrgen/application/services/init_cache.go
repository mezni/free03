package services

import (
	"errors"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore" 
)

// InitCacheService structure to hold service state
type InitCacheService struct {
	db         *boltstore.BoltDBConfig
	repository *inmemstore.InMemoryNetworkTechnologyRepository 
}

// NewInitCacheService constructor for InitCacheService
func NewInitCacheService() (*InitCacheService, error) {
	// Initialize BoltDBConfig and open the database file
	boltDBConfig := boltstore.NewBoltDBConfig()
	if err := boltDBConfig.Open(dbPath); err != nil {
		return nil, errors.New("failed to open database")
	}

	// Initialize the in-memory repository
	repository := inmemstore.NewInMemoryNetworkTechnologyRepository()

	return &InitCacheService{
		db:         boltDBConfig,
		repository: repository,
	}, nil
}

// InitCache initializes and loads the cache data from the database
func (service *InitCacheService) InitCache() error {
	if service.db == nil {
		return fmt.Errorf("database connection is not initialized")
	}

	// Read data from the specified bucket
	data, err := service.db.ReadFromBoltDB(networkTechnologiesBucketName)
	if err != nil {
		return fmt.Errorf("failed to read from bucket '%s': %w", networkTechnologiesBucketName, err)
	}

	// Convert the data from map to NetworkTechnology entities and save to repository
	for _, item := range data {
		var networkTech entities.NetworkTechnology
		err := mappers.MapToEntity(item, &networkTech)
		if err != nil {
			return fmt.Errorf("failed to convert map to NetworkTechnology: %w", err)
		}

		// Add the converted entity to the repository
		err = service.repository.Create(networkTech)
		if err != nil {
			return fmt.Errorf("failed to add NetworkTechnology to repository: %w", err)
		}
	}

	// Optionally log or process the stored data (e.g., load all from the repository)
	technologies, err := service.repository.GetAll()
	if err != nil {
		return fmt.Errorf("failed to retrieve all NetworkTechnologies: %w", err)
	}

	// Log the loaded technologies (for debugging purposes)
	fmt.Printf("Loaded Network Technologies from repository: %v\n", technologies)
	return nil
}
