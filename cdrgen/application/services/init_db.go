package services

import (
	"errors"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"github.com/mezni/wovoka/cdrgen/infrastructure/filestore"
	"os"
)

// Constants for database path and bucket names
const dbPath = "./db/mydb.db"
const (
	networkTechnologiesBucketName = "network_technologies"
	networkElementTypesBucketName = "network_element_types"
	serviceTypesBucketName        = "service_types"
)

// InitDBService structure to hold service state
type InitDBService struct {
	configFile string
	db         *boltstore.BoltDBConfig
}

// NewInitDBService constructor for InitDBService
// The constructor accepts the configFile as an argument
func NewInitDBService(configFile string) (*InitDBService, error) {
	// Check if the config file exists and the database file doesn't exist
	if err := checkFileExistence(configFile, dbPath); err != nil {
		return nil, err
	}

	// Initialize BoltDBConfig and create the database file using the Create method
	boltDBConfig := boltstore.NewBoltDBConfig()
	if err := boltDBConfig.Create(dbPath); err != nil {
		return nil, err
	}

	// Return the service instance with the database and configFile
	return &InitDBService{
		configFile: configFile,
		db:         boltDBConfig,
	}, nil
}

// checkFileExistence checks if the provided file exists and returns appropriate error
func checkFileExistence(configFile, dbPath string) error {
	// Check if the config file exists
	if _, err := os.Stat(configFile); os.IsNotExist(err) {
		return errors.New("config file '" + configFile + "' does not exist")
	}

	// Check if the database file already exists
	if _, err := os.Stat(dbPath); err == nil {
		return errors.New("database file '" + dbPath + "' already exists")
	}

	return nil
}

// InitDB initializes the database by reading the configuration and processing it
func (service *InitDBService) InitDB() error {
	// Read the config file in JSON format
	data, err := filestore.ReadJSONFromFile(service.configFile)
	if err != nil {
		return fmt.Errorf("error reading JSON file: %w", err)
	}

	// Decode the JSON data into the BaselineConfig struct
	var baselineConfig dtos.BaselineConfig
	if err := mappers.MapToStruct(data, &baselineConfig); err != nil {
		return fmt.Errorf("error decoding JSON into struct: %w", err)
	}

	// Process and save different data types into their respective buckets
	if err := processAndSaveData[dtos.NetworkTechnologyDTO](baselineConfig.NetworkTechnologies, networkTechnologiesBucketName, service.db); err != nil {
		return fmt.Errorf("error processing network technologies: %w", err)
	}

	if err := processAndSaveData[dtos.NetworkElementTypeDTO](baselineConfig.NetworkElementTypes, networkElementTypesBucketName, service.db); err != nil {
		return fmt.Errorf("error processing network element types: %w", err)
	}

	if err := processAndSaveData[dtos.ServiceTypeDTO](baselineConfig.ServiceTypes, serviceTypesBucketName, service.db); err != nil {
		return fmt.Errorf("error processing service types: %w", err)
	}

	return nil
}

// processAndSaveData is a generic function to process and save data to the BoltDB database
func processAndSaveData[T any](data interface{}, bucketName string, db *boltstore.BoltDBConfig) error {
	// Type assertion to []T (generic type)
	slice, ok := data.([]T)
	if !ok {
		return fmt.Errorf("data is not of type []%T", *new(T))
	}

	// Convert the slice to a slice of maps
	dataAsMaps, err := mappers.ConvertSliceToMaps[T](slice)
	if err != nil {
		return fmt.Errorf("error converting slice to maps: %w", err)
	}

	// Save the processed data to the database
	if err := db.SaveToBoltDB(bucketName, dataAsMaps); err != nil {
		return fmt.Errorf("error saving data to database: %w", err)
	}

	return nil
}
