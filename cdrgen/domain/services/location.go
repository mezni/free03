package services

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/domain/repositories"
)

type NetworkConfig struct {
	Rows          int
	Columns       int
	LocationNames []string
}

type CountryConfig struct {
	Country   string
	Latitude  [2]float64
	Longitude [2]float64
	Networks  map[string]NetworkConfig
}

// LocationService struct to handle location creation logic.
type LocationService struct {
	config     CountryConfig
	repository repositories.LocationRepository
}

// NewLocationService creates a new LocationService from a config file path and repository.
func NewLocationService(configFilePath string, repo repositories.LocationRepository) (*LocationService, error) {
	file, err := os.Open(configFilePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var config CountryConfig
	decoder := json.NewDecoder(file)
	err = decoder.Decode(&config)
	if err != nil {
		return nil, err
	}

	return &LocationService{
		config:     config,
		repository: repo,
	}, nil
}

// GenerateLocations generates location entities based on the provided configuration and saves them to the repository.
func (service *LocationService) GenerateLocations() ([]*entities.Location, error) {
	var locations []*entities.Location

	// Iterate over each network configuration (e.g., 2G, 3G)
	for _, networkConfig := range service.config.Networks {
		for i := 0; i < networkConfig.Rows; i++ {
			for j := 0; j < networkConfig.Columns; j++ {
				// Calculate the latitude and longitude range for each cell
				latitudeMin := service.config.Latitude[0] + float64(i)*(service.config.Latitude[1]-service.config.Latitude[0])/float64(networkConfig.Rows)
				latitudeMax := service.config.Latitude[0] + float64(i+1)*(service.config.Latitude[1]-service.config.Latitude[0])/float64(networkConfig.Rows)
				longitudeMin := service.config.Longitude[0] + float64(j)*(service.config.Longitude[1]-service.config.Longitude[0])/float64(networkConfig.Columns)
				longitudeMax := service.config.Longitude[0] + float64(j+1)*(service.config.Longitude[1]-service.config.Longitude[0])/float64(networkConfig.Columns)

				// Assign a location name from the locationNames array in the config
				locationName := ""
				if len(networkConfig.LocationNames) > 0 {
					locationName = networkConfig.LocationNames[(i+j)%len(networkConfig.LocationNames)] // Cyclic use of location names
				}

				// Generate a new location
				location, err := entities.NewLocation(
					i*100+j,                   // A unique ID for the location, could be adjusted
					entities.NetworkType(i%4), // Map i to a network type (assuming 4 types)
					locationName,
					latitudeMin, latitudeMax, longitudeMin, longitudeMax,
				)
				if err != nil {
					return nil, fmt.Errorf("error creating location: %v", err)
				}

				// Save the location to the repository
				err = service.repository.Create(location)
				if err != nil {
					return nil, fmt.Errorf("error saving location: %v", err)
				}

				locations = append(locations, location)
			}
		}
	}

	return locations, nil
}

// GetAllLocations retrieves all locations from the repository.
func (service *LocationService) GetAllLocations() ([]*entities.Location, error) {
	return service.repository.GetAll()
}

// GetRandomLocationByNetworkType retrieves a random location based on the network type.
func (service *LocationService) GetRandomLocationByNetworkType(networkType entities.NetworkType) (*entities.Location, error) {
	return service.repository.GetRandomByNetworkType(networkType)
}
