package services

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"

	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
)

// Custom error definitions
var (
	ErrFailedToOpenFile     = errors.New("failed to open JSON")
	ErrFailedToDecodeJson   = errors.New("failed to decode JSON")
	ErrFailedToSaveToBolt   = errors.New("failed to save to BoltDB")
	ErrDataConversion       = errors.New("failed to convert data")
	ErrFailedToLoadConfig   = errors.New("failed to load configuration")
	ErrFailedToProcessData  = errors.New("failed to process and save data")
	ErrFailedToSaveData     = errors.New("failed to save data")
)

// InitDBService holds the configuration file and database file information.
type InitDBService struct {
	configFile string
	dbFile     string
}

// NewInitDBService creates a new instance of InitDBService with config and db file paths.
func NewInitDBService(configFile, dbFile string) *InitDBService {
	return &InitDBService{
		configFile: configFile,
		dbFile:     dbFile,
	}
}

// LoadConfig loads the baseline configuration from the JSON file.
func (s *InitDBService) LoadConfig() (dtos.BaselineConfig, error) {
	// Open the JSON config file
	file, err := os.Open(s.configFile)
	if err != nil {
		return dtos.BaselineConfig{}, ErrFailedToOpenFile
	}
	defer file.Close()

	// Decode JSON into BaselineConfig struct
	var config dtos.BaselineConfig
	if err := json.NewDecoder(file).Decode(&config); err != nil {
		return dtos.BaselineConfig{}, ErrFailedToDecodeJson
	}
	return config, nil
}

// createBoltDBConfig generates a BoltDBConfig with a given bucket name.
func createBoltDBConfig(dbFile, bucketName string) boltstore.BoltDBConfig {
	return boltstore.BoltDBConfig{
		DBName:     dbFile,
		BucketName: bucketName,
	}
}

// saveToBoltDB is a helper function to handle saving data to the BoltDB database.
func saveToBoltDB(dbFile, bucketName string, data []map[string]interface{}) error {
	// Create BoltDB configuration
	config := createBoltDBConfig(dbFile, bucketName)

	// Save to BoltDB
	err := boltstore.SaveToBoltDB(config, data)
	if err != nil {
		return ErrFailedToSaveToBolt
	}

	fmt.Printf("%s saved to BoltDB successfully.\n", bucketName)
	return nil
}

// processAndSaveData is a general function to process any configuration type (e.g., NetworkTechnologies, NetworkElementTypes, ServiceTypes) and save it.
func processAndSaveData[T any](dbFile, bucketName string, dataSlice []T) error {
	// Convert the data slice to a list of maps
	dataAsMaps, err := mappers.ConvertSliceToMaps(dataSlice)
	if err != nil {
		return ErrDataConversion
	}

	// Debug: Print the list of maps
	fmt.Printf("Converted %s:\n", bucketName)
	for _, dataMap := range dataAsMaps {
		fmt.Printf("  %+v\n", dataMap)
	}

	// Save to BoltDB using the helper function
	err = saveToBoltDB(dbFile, bucketName, dataAsMaps)
	if err != nil {
		return fmt.Errorf("%w: %s", ErrFailedToSaveData, bucketName)
	}

	return nil
}

// InitializeDB initializes the database by processing different configuration data types and saving them to BoltDB.
func (s *InitDBService) InitializeDB() error {
	// Load the configuration data
	configData, err := s.LoadConfig()
	if err != nil {
		return fmt.Errorf("%w: %v", ErrFailedToLoadConfig, err)
	}

	// Process and save Network Technologies
	err = processAndSaveData(s.dbFile, "network_technologies", configData.NetworkTechnologies)
	if err != nil {
		return fmt.Errorf("%w: network technologies", err)
	}

	// Process and save Network Element Types
	err = processAndSaveData(s.dbFile, "network_element_types", configData.NetworkElementTypes)
	if err != nil {
		return fmt.Errorf("%w: network element types", err)
	}

	// Process and save Service Types
	err = processAndSaveData(s.dbFile, "service_types", configData.ServiceTypes)
	if err != nil {
		return fmt.Errorf("%w: service types", err)
	}

	return nil
}
