package services

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
)

const (
	networkTechnologiesBucket = "network_technologies"
	networkElementTypesBucket = "network_element_types"
	serviceTypesBucket        = "service_types"
)

type BaselineLoaderService struct {
	configFile string
	dbFile     string
}

func NewBaselineLoaderService(configFile, dbFile string) *BaselineLoaderService {
	return &BaselineLoaderService{
		configFile: configFile,
		dbFile:     dbFile,
	}
}

// LoadConfig loads the baseline configuration from the JSON file.
func (ls *BaselineLoaderService) LoadConfig() (dtos.BaselineConfig, error) {
	// Open the JSON config file
	file, err := os.Open(ls.configFile)
	if err != nil {
		return dtos.BaselineConfig{}, fmt.Errorf("error opening config file: %w", err)
	}
	defer file.Close()

	// Decode JSON into BaselineConfig struct
	var config dtos.BaselineConfig
	if err := json.NewDecoder(file).Decode(&config); err != nil {
		return dtos.BaselineConfig{}, fmt.Errorf("error decoding JSON: %w", err)
	}
	return config, nil
}

// LoadBaseline processes the baseline configuration.
func (ls *BaselineLoaderService) LoadBaseline() error {
	// Step 1: Load the configuration
	config, err := ls.LoadConfig()
	if err != nil {
		return fmt.Errorf("error loading configuration: %w", err)
	}

	// Step 2: Create a BaselineMapper instance
	mapper := &mappers.BaselineMapper{}

	// Step 3: Map DTOs to domain entities for network technologies
	networkTechnologies, err := mapper.ToNetworkTechnologies(config.NetworkTechnologies)
	if err != nil {
		return fmt.Errorf("error mapping network technologies: %w", err)
	}

	// Step 4: Convert networkTechnologies to []interface{} for saving in BoltDB
	networkTechnologiesAsInterfaces := make([]interface{}, len(networkTechnologies))
	for i, loc := range networkTechnologies {
		networkTechnologiesAsInterfaces[i] = loc
	}

	// Step 5: Save network technologies to BoltDB
	err = boltstore.SaveToBoltDB(ls.dbFile, networkTechnologiesBucket, networkTechnologiesAsInterfaces)
	if err != nil {
		return fmt.Errorf("error saving network technologies to DB: %w", err)
	}

	// Step 6: Map DTOs to domain entities for network element types
	networkElementTypes, err := mapper.ToNetworkElementTypes(config.NetworkElementTypes)
	if err != nil {
		return fmt.Errorf("error mapping network element types: %w", err)
	}

	// Step 7: Convert networkElementTypes to []interface{} for saving in BoltDB
	networkElementTypesAsInterfaces := make([]interface{}, len(networkElementTypes))
	for i, loc := range networkElementTypes {
		networkElementTypesAsInterfaces[i] = loc
	}

	// Step 8: Save network element types to BoltDB
	err = boltstore.SaveToBoltDB(ls.dbFile, networkElementTypesBucket, networkElementTypesAsInterfaces)
	if err != nil {
		return fmt.Errorf("error saving network element types to DB: %w", err)
	}

	// Step 9: Map DTOs to domain entities for service types
	serviceTypes, err := mapper.ToServiceTypes(config.ServiceTypes)
	if err != nil {
		return fmt.Errorf("error mapping service types: %w", err)
	}

	// Step 10: Convert serviceTypes to []interface{} for saving in BoltDB
	serviceTypesAsInterfaces := make([]interface{}, len(serviceTypes))
	for i, loc := range serviceTypes {
		serviceTypesAsInterfaces[i] = loc
	}

	// Step 11: Save service types to BoltDB
	err = boltstore.SaveToBoltDB(ls.dbFile, serviceTypesBucket, serviceTypesAsInterfaces)
	if err != nil {
		return fmt.Errorf("error saving service types to DB: %w", err)
	}

	return nil
}
