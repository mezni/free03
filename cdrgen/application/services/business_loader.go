package services

import (
	"encoding/json"
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
	"go.etcd.io/bbolt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// Config struct for parsing YAML
type Config struct {
	Country     string
	Coordinates struct {
		Latitude  [2]float64
		Longitude [2]float64
	}
	Networks map[string]struct {
		Rows          int
		Columns       int
		LocationNames []string
	}
}

// BusinessLoaderService defines the service for loading business data
type BusinessLoaderService struct {
	DB *bbolt.DB // bbolt instance to persist data
}

// LoadData loads business data from a YAML file, processes it, and saves it to the database
func (b *BusinessLoaderService) LoadData(filename string) error {
	// Check if the file exists
	if _, err := os.Stat(filename); os.IsNotExist(err) {
		return fmt.Errorf("file does not exist: %v", filename)
	}

	// Read the YAML file
	data, err := os.ReadFile(filename)
	if err != nil {
		return fmt.Errorf("could not read file: %v", err)
	}

	// Parse YAML into Config struct
	var config Config
	if err := yaml.Unmarshal(data, &config); err != nil {
		return fmt.Errorf("could not unmarshal yaml: %v", err)
	}

	// Log the parsed config for debugging
	fmt.Printf("Parsed Config: %+v\n", config)

	// Generate locations from config
	locations, err := generateLocations(&config)
	if err != nil {
		return fmt.Errorf("error generating locations: %v", err)
	}

	// If locations are empty, log the issue
	if len(locations) == 0 {
		return fmt.Errorf("no locations were generated")
	}

	// Save locations to BoltDB
	if err := b.saveLocationsToDB(locations); err != nil {
		return fmt.Errorf("error saving locations to DB: %v", err)
	}

	return nil
}


// generateLocations creates location entities based on the configuration
func generateLocations(config *Config) ([]*entities.Location, error) {
	var locations []*entities.Location
	locationID := 1

	for networkType, networkData := range config.Networks {
		latRange := config.Coordinates.Latitude[1] - config.Coordinates.Latitude[0]
		lonRange := config.Coordinates.Longitude[1] - config.Coordinates.Longitude[0]

		latStep := latRange / float64(networkData.Rows)
		lonStep := lonRange / float64(networkData.Columns)

		if len(networkData.LocationNames) != networkData.Rows*networkData.Columns {
			return nil, fmt.Errorf("mismatch between location names and grid dimensions for network %s", networkType)
		}

		// Generate grid locations
		index := 0
		for row := 0; row < networkData.Rows; row++ {
			for col := 0; col < networkData.Columns; col++ {
				latMin := config.Coordinates.Latitude[0] + latStep*float64(row)
				latMax := latMin + latStep
				lonMin := config.Coordinates.Longitude[0] + lonStep*float64(col)
				lonMax := lonMin + lonStep

				locationName := networkData.LocationNames[index]
				index++

				// Create a new Location instance
				location, err := entities.NewLocation(
					locationID,
					networkType,
					locationName,
					latMin, latMax,
					lonMin, lonMax,
					fmt.Sprintf("%04d", locationID), // Area code as a 4-digit string
				)
				if err != nil {
					return nil, fmt.Errorf("error creating location %d for network %s: %v", locationID, networkType, err)
				}

				locations = append(locations, location)
				locationID++
			}
		}
	}

	return locations, nil
}

// saveLocationsToDB saves the generated locations to BoltDB
func (b *BusinessLoaderService) saveLocationsToDB(locations []*entities.Location) error {
	return b.DB.Update(func(tx *bbolt.Tx) error {
		bucket, err := tx.CreateBucketIfNotExists([]byte("locations"))
		if err != nil {
			return fmt.Errorf("could not create bucket: %v", err)
		}

		for _, location := range locations {
			key := fmt.Sprintf("%d", location.LocationID)
			value, err := json.Marshal(location)
			if err != nil {
				return fmt.Errorf("could not marshal location: %v", err)
			}

			if err := bucket.Put([]byte(key), value); err != nil {
				return fmt.Errorf("could not save location: %v", err)
			}
		}

		return nil
	})
}
