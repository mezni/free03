package services

import (
	"errors"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
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

	// Initialize the in-memory repository (generic repository)
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

	// Process network technologies data by reading from the database, converting, and saving to the repository
	err := service.processNetworkTechnologies()
	if err != nil {
		return fmt.Errorf("failed to process network technologies: %w", err)
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

// processNetworkTechnologies is a function that encapsulates the entire process of reading data, converting it to entities, and saving it to the repository.
func (service *InitCacheService) processNetworkTechnologies() error {
	bucketName := networkTechnologiesBucketName

	data, err := service.readDataFromBucket(bucketName)
	if err != nil {
		return err
	}

	networkTechnologies, err := service.convertDataToEntities(data)
	if err != nil {
		return err
	}

	err = service.saveToRepository(networkTechnologies)
	if err != nil {
		return err
	}

	return nil
}

// readDataFromBucket reads data from the specified bucket in the database.
func (service *InitCacheService) readDataFromBucket(bucketName string) ([]map[string]interface{}, error) {
	data, err := service.db.ReadFromBoltDB(bucketName)
	if err != nil {
		return nil, fmt.Errorf("failed to read from bucket '%s': %w", bucketName, err)
	}
	return data, nil
}

// convertDataToEntities converts raw data to entities of type T.
func (service *InitCacheService) convertDataToEntities(data []map[string]interface{}) ([]entities.NetworkTechnology, error) {
	var networkTechnologies []entities.NetworkTechnology
	for _, item := range data {
		var networkTech entities.NetworkTechnology
		err := mappers.MapToEntity(item, &networkTech)
		if err != nil {
			return nil, fmt.Errorf("failed to convert map to NetworkTechnology: %w", err)
		}
		networkTechnologies = append(networkTechnologies, networkTech)
	}
	return networkTechnologies, nil
}

// saveToRepository saves the converted entities to the repository.
func (service *InitCacheService) saveToRepository(networkTechnologies []entities.NetworkTechnology) error {
	for _, networkTech := range networkTechnologies {
		err := service.repository.Create(networkTech)
		if err != nil {
			return fmt.Errorf("failed to add NetworkTechnology to repository: %w", err)
		}
	}
	return nil
}
