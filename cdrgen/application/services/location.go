package services

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/config"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
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
func (ls *LoaderService) LoadConfig() (config.CfgData, error) {
	cfg, err := config.LoadConfig(ls.configFile)
	if err != nil {
		return config.CfgData{}, fmt.Errorf("failed to load configuration: %v", err)
	}
	return cfg, nil
}

// LoadLocations reads locations from the database using the provided dbName
func (ls *LoaderService) LoadLocations(dbName string) error {
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

	// Save generated locations to BoltDB
	err = boltstore.SaveToBoltDB(dbName, "locations", locations)
	if err != nil {
		return fmt.Errorf("error saving locations to DB: %v", err)
	}

	return nil
}
