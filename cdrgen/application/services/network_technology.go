package services

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// NetworkTechnologyServiceInter defines the operations for managing network technologies.
type NetworkTechnologyServiceInter interface {
	// SaveToDatabase saves a list of NetworkTechnology instances to the BoltDB.
	SaveToDatabase(networkTechnologies []*entities.NetworkTechnology) error
	
	// ReadFromDatabase retrieves all NetworkTechnology instances from BoltDB.
	ReadFromDatabase() ([]*entities.NetworkTechnology, error)
}

// NetworkTechnologyService is the implementation of the NetworkTechnologyServiceInter interface.
type NetworkTechnologyService struct {
	Repository boltstore.BoltDBConfig
	Mapper     *mappers.NetworkTechnologyMapper
}

// NewNetworkTechnologyService creates a new instance of the service with the provided configuration.
func NewNetworkTechnologyService(repository boltstore.BoltDBConfig, mapper *mappers.NetworkTechnologyMapper) NetworkTechnologyServiceInter {
	return &NetworkTechnologyService{
		Repository: repository,
		Mapper:     mapper,
	}
}

// SaveToDatabase saves a list of NetworkTechnology instances to the BoltDB.
func (service *NetworkTechnologyService) SaveToDatabase(networkTechnologies []*entities.NetworkTechnology) error {
	// Convert NetworkTechnology structs to maps using the ToListMap method
	data := service.Mapper.ToListMap(networkTechnologies)

	// Save data to BoltDB
	fmt.Println("Saving data to BoltDB...")
	err := boltstore.SaveToBoltDB(service.Repository, data)
	if err != nil {
		return fmt.Errorf("error saving to BoltDB: %v", err)
	}
	fmt.Println("Data saved successfully.")
	return nil
}

// ReadFromDatabase retrieves all NetworkTechnology instances from BoltDB.
func (service *NetworkTechnologyService) ReadFromDatabase() ([]*entities.NetworkTechnology, error) {
	// Read data from BoltDB
	fmt.Println("Reading data from BoltDB...")
	entitiesMap, err := boltstore.ReadFromBoltDB(service.Repository)
	if err != nil {
		return nil, fmt.Errorf("error reading from BoltDB: %v", err)
	}

	// Convert maps to NetworkTechnology structs using the mapper
	networkTechnologies := make([]*entities.NetworkTechnology, len(entitiesMap))
	for i, item := range entitiesMap {
		nt, err := service.Mapper.FromMap(item)
		if err != nil {
			return nil, fmt.Errorf("error converting map to NetworkTechnology: %v", err)
		}
		networkTechnologies[i] = nt
	}

	fmt.Println("Data read successfully.")
	return networkTechnologies, nil
}
