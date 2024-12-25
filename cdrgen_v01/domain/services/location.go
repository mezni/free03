package services

import (
	"encoding/json"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"time"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/domain/repositories"
)

type Coordinates struct {
	Latitude  [2]float64 `json:"Latitude"`
	Longitude [2]float64 `json:"Longitude"`
}

type NetworkConfig struct {
	Rows          int
	Columns       int
	LocationNames []string
}

type CountryConfig struct {
	Country     string                   `json:"Country"`
	Coordinates Coordinates              `json:"Coordinates"`
	Networks    map[string]NetworkConfig `json:"Networks"`
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

	// Debugging: Print out the loaded configuration
	fmt.Printf("Loaded config: %+v\n", config)

	return &LocationService{
		config:     config,
		repository: repo,
	}, nil
}

// GenerateLocations generates location entities based on the provided configuration and saves them to the repository.
func (service *LocationService) GenerateLocations() ([]*entities.Location, error) {
	var locations []*entities.Location

	// Initialize a counter for unique LocationID
	locationIDCounter := 1

	// Initialize random seed for AreaCode generation
	rand.Seed(time.Now().UnixNano())

	// Iterate over each network configuration (e.g., 2G, 3G, 4G)
	for networkTypeStr, networkConfig := range service.config.Networks {
		// Determine the network type
		var networkType entities.NetworkType
		switch networkTypeStr {
		case "2G":
			networkType = entities.NetworkType2G
		case "3G":
			networkType = entities.NetworkType3G
		case "4G":
			networkType = entities.NetworkType4G
		case "5G":
			networkType = entities.NetworkType5G
		default:
			return nil, fmt.Errorf("unsupported network type: %s", networkTypeStr)
		}

		for i := 0; i < networkConfig.Rows; i++ {
			for j := 0; j < networkConfig.Columns; j++ {
				// Calculate the latitude and longitude range for each cell
				latitudeMin := service.config.Coordinates.Latitude[0] + float64(i)*(service.config.Coordinates.Latitude[1]-service.config.Coordinates.Latitude[0])/float64(networkConfig.Rows)
				latitudeMax := service.config.Coordinates.Latitude[0] + float64(i+1)*(service.config.Coordinates.Latitude[1]-service.config.Coordinates.Latitude[0])/float64(networkConfig.Rows)
				longitudeMin := service.config.Coordinates.Longitude[0] + float64(j)*(service.config.Coordinates.Longitude[1]-service.config.Coordinates.Longitude[0])/float64(networkConfig.Columns)
				longitudeMax := service.config.Coordinates.Longitude[0] + float64(j+1)*(service.config.Coordinates.Longitude[1]-service.config.Coordinates.Longitude[0])/float64(networkConfig.Columns)

				// Assign a location name from the locationNames array in the config
				locationName := ""
				if len(networkConfig.LocationNames) > 0 {
					locationName = networkConfig.LocationNames[(i+j)%len(networkConfig.LocationNames)] // Cyclic use of location names
				}

				// Generate AreaCode based on network type (first digit) and a random 3-digit number
				var networkPrefix string
				switch networkType {
				case entities.NetworkType2G:
					networkPrefix = "2"
				case entities.NetworkType3G:
					networkPrefix = "3"
				case entities.NetworkType4G:
					networkPrefix = "4"
				case entities.NetworkType5G:
					networkPrefix = "5"
				}
				// Generate a random 3-digit number
				randomNumber := rand.Intn(1000)                                // Generate random number between 0 and 999
				areaCode := fmt.Sprintf("%s%03d", networkPrefix, randomNumber) // Ensures 3-digit random number

				// Convert AreaCode from string to int
				areaCodeInt, err := strconv.Atoi(areaCode)
				if err != nil {
					return nil, fmt.Errorf("error converting AreaCode to int: %v", err)
				}

				// Generate a new location with the incremented LocationID
				location, err := entities.NewLocation(
					locationIDCounter, // Use the global counter for LocationID
					networkType,       // Use the determined network type
					locationName,
					latitudeMin, latitudeMax, longitudeMin, longitudeMax,
					areaCodeInt, // Pass the calculated AreaCode as an int
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

				// Increment the location ID counter for the next location
				locationIDCounter++
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

// GenerateAreaCode generates an area code based on the network type.
func (service *LocationService) GenerateAreaCode(networkType entities.NetworkType) (int, error) {
	// Initialize random seed for AreaCode generation
	rand.Seed(time.Now().UnixNano())

	// Generate the area code based on network type (first digit) and a random 3-digit number
	var networkPrefix string
	switch networkType {
	case entities.NetworkType2G:
		networkPrefix = "2"
	case entities.NetworkType3G:
		networkPrefix = "3"
	case entities.NetworkType4G:
		networkPrefix = "4"
	case entities.NetworkType5G:
		networkPrefix = "5"
	default:
		return 0, fmt.Errorf("unsupported network type: %v", networkType)
	}

	// Generate a random 3-digit number
	randomNumber := rand.Intn(1000) // Generate random number between 0 and 999

	// Form the area code (networkPrefix + random 3-digit number)
	areaCode := fmt.Sprintf("%s%03d", networkPrefix, randomNumber)

	// Convert area code to an integer
	areaCodeInt, err := strconv.Atoi(areaCode)
	if err != nil {
		return 0, fmt.Errorf("error converting AreaCode to int: %v", err)
	}

	return areaCodeInt, nil
}
