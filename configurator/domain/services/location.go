package services

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/mezni/wovoka/configurator/domain/entities"
	"github.com/mezni/wovoka/configurator/domain/repositories"
	"os"
)

// NetworkConfig represents the configuration for network settings.
type NetworkConfig struct {
	Rows          int      `json:"rows"`
	Columns       int      `json:"columns"`
	LocationNames []string `json:"locationNames"`
}

// CountryConfig represents the configuration for the country in which locations are generated.
type CountryConfig struct {
	Country   string             `json:"country"`
	Latitude  [2]float64        `json:"latitude"`
	Longitude [2]float64        `json:"longitude"`
	Networks  map[string]NetworkConfig `json:"networks"`
}

// LocationService struct handles the business logic for location creation and manipulation.
type LocationService struct {
	config     CountryConfig
	repository repositories.LocationRepository
}

// NewLocationService creates a new LocationService instance, loading the config from a file.
func NewLocationService(configFilePath string, repo repositories.LocationRepository) (*LocationService, error) {
	config, err := loadConfig(configFilePath)
	if err != nil {
		return nil, err
	}

	return &LocationService{
		config:     config,
		repository: repo,
	}, nil
}

// loadConfig loads the configuration from the given file path.
func loadConfig(configFilePath string) (CountryConfig, error) {
	file, err := os.Open(configFilePath)
	if err != nil {
		return CountryConfig{}, fmt.Errorf("failed to open config file: %v", err)
	}
	defer file.Close()

	var config CountryConfig
	decoder := json.NewDecoder(file)
	err = decoder.Decode(&config)
	if err != nil {
		return CountryConfig{}, fmt.Errorf("failed to decode config file: %v", err)
	}

	// Validate the configuration
	if err := validateConfig(config); err != nil {
		return CountryConfig{}, err
	}

	return config, nil
}

// validateConfig ensures the configuration is valid.
func validateConfig(config CountryConfig) error {
	if config.Country == "" {
		return errors.New("country is required")
	}
	if len(config.Networks) == 0 {
		return errors.New("at least one network configuration is required")
	}
	if config.Latitude[0] >= config.Latitude[1] || config.Longitude[0] >= config.Longitude[1] {
		return errors.New("invalid latitude or longitude range")
	}
	return nil
}

// GenerateLocations generates location entities based on the configuration and stores them in the repository.
func (service *LocationService) GenerateLocations() ([]*entities.Location, error) {
	var locations []*entities.Location

	// Iterate over each network configuration (e.g., 2G, 3G, etc.)
	for networkName, networkConfig := range service.config.Networks {
		for i := 0; i < networkConfig.Rows; i++ {
			for j := 0; j < networkConfig.Columns; j++ {
				// Calculate latitude and longitude range for each cell
				latitudeMin := service.config.Latitude[0] + float64(i)*(service.config.Latitude[1]-service.config.Latitude[0])/float64(networkConfig.Rows)
				latitudeMax := service.config.Latitude[0] + float64(i+1)*(service.config.Latitude[1]-service.config.Latitude[0])/float64(networkConfig.Rows)
				longitudeMin := service.config.Longitude[0] + float64(j)*(service.config.Longitude[1]-service.config.Longitude[0])/float64(networkConfig.Columns)
				longitudeMax := service.config.Longitude[0] + float64(j+1)*(service.config.Longitude[1]-service.config.Longitude[0])/float64(networkConfig.Columns)

				// Assign a location name from the config (cyclic behavior)
				locationName := ""
				if len(networkConfig.LocationNames) > 0 {
					locationName = networkConfig.LocationNames[(i+j)%len(networkConfig.LocationNames)]
				}

				// Create a new Location
				location, err := entities.NewLocation(
					i*100+j,                  // Unique ID for the location
					entities.NetworkType(i%4), // Map i to network type (assuming 4 types)
					locationName,
					latitudeMin, latitudeMax, longitudeMin, longitudeMax,
				)
				if err != nil {
					return nil, fmt.Errorf("error creating location: %v", err)
				}

				// Save the location to the repository
				if err := service.repository.Create(location); err != nil {
					return nil, fmt.Errorf("error saving location: %v", err)
				}

				// Add to the locations list
				locations = append(locations, location)
			}
		}
	}

	return locations, nil
}
