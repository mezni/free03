package services

import (
	"encoding/json"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/infrastructure/config"
)

type LoaderService struct {
	configFile string
	dbFile     string
}

// NewLoaderService initializes and returns a new instance of LoaderService
func NewLoaderService(configFile, dbFile string) *LoaderService {
	return &LoaderService{
		configFile: configFile,
		dbFile:     dbFile,
	}
}

// LoadConfig loads the configuration from the provided config file
func (ls *LoaderService) LoadConfig() (dtos.CfgData, error) {
	cfg, err := config.LoadConfig(ls.configFile)
	if err != nil {
		return dtos.CfgData{}, fmt.Errorf("failed to load configuration: %v", err)
	}
	return cfg, nil
}

// LoadLocations reads locations from the database and saves them
func (ls *LoaderService) LoadLocations() error {
	// Load the configuration first
	cfg, err := ls.LoadConfig()
	if err != nil {
		return fmt.Errorf("error loading config: %v", err)
	}

	// Initialize LocationService to generate locations
	locationService := mappers.NewLocationService()

	// Generate locations
	locations, err := locationService.GenerateLocations(cfg)
	if err != nil {
		return fmt.Errorf("error generating locations: %v", err)
	}

	// Convert []entities.Location to []interface{}
	var locationsAsInterfaces []interface{}
	for _, loc := range locations {
		locationsAsInterfaces = append(locationsAsInterfaces, loc)
	}

	// Save generated locations to BoltDB using the dbFile from LoaderService
	err = boltstore.SaveToBoltDB(ls.dbFile, "locations", locationsAsInterfaces)
	if err != nil {
		return fmt.Errorf("error saving locations to DB: %v", err)
	}

	return nil
}

func (ls *LoaderService) DumpLocations() ([]entities.Location, error) {
	// Read the locations from the database using the dbFile from LoaderService
	locationsAsInterfaces, err := boltstore.ReadFromBoltDB(ls.dbFile, "locations")
	if err != nil {
		return nil, fmt.Errorf("error reading locations from DB: %v", err)
	}

	// Convert []interface{} to []entities.Location
	var locations []entities.Location
	for _, loc := range locationsAsInterfaces {

		// Convert map[string]interface{} to entities.Location
		locMap, ok := loc.(map[string]interface{})
		if !ok {
			return nil, fmt.Errorf("failed to cast item to map[string]interface{}, got: %T", loc)
		}

		// Unmarshal the map into a Location object
		var location entities.Location
		data, err := json.Marshal(locMap)
		if err != nil {
			return nil, fmt.Errorf("failed to marshal map to JSON: %v", err)
		}

		err = json.Unmarshal(data, &location)
		if err != nil {
			return nil, fmt.Errorf("failed to unmarshal map to Location: %v", err)
		}

		locations = append(locations, location)
	}

	return locations, nil
}
