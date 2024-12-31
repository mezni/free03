package services

import (
	"errors"
	"github.com/mezni/wovoka/cdrgen/infrastructure/filestore"
	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
	"os"
)

// Define dbPath as a constant with the relative path
const dbPath = "./db/mydb.db" // Database file path as a constant

// InitDBService structure to hold service state
type InitDBService struct {
	configFile string
	db         *boltstore.BoltDBConfig // Use the BoltDBConfig type from boltstore package
}

// NewInitDBService constructor for InitDBService
// The constructor now only accepts the configFile as an argument
func NewInitDBService(configFile string) (*InitDBService, error) {
	// Check if the config file exists and database file doesn't exist
	if err := checkFileExistence(configFile, dbPath); err != nil {
		return nil, err
	}

	// Initialize BoltDBConfig and create the database file using Create method
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
	if _, err := os.Stat(configFile); os.IsNotExist(err) {
		return errors.New("config file '" + configFile + "' does not exist")
	}
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
		return errors.New("error reading JSON file: " + err.Error())
	}

	// Decode the JSON data into the BaselineConfig struct
	var baselineConfig dtos.BaselineConfig
	if err := mappers.MapToStruct(data, &baselineConfig); err != nil {
		return errors.New("error decoding JSON into struct: " + err.Error())
	}

	// Further database initialization logic can go here (e.g., creating buckets)
	// You can process baselineConfig or take other actions as needed.

	return nil
}
