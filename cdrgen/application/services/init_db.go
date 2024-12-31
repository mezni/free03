package services

import (
	"encoding/json"
	"errors"
	"fmt"
	"os"

	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	// "github.com/mezni/wovoka/cdrgen/domain/entities"
)

// Custom error definitions
var (
	ErrOpenFile   = errors.New("error opening JSON")
	ErrDecodeJson = errors.New("error decoding JSON")
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
		return dtos.BaselineConfig{}, ErrOpenFile
	}
	defer file.Close()

	// Decode JSON into BaselineConfig struct
	var config dtos.BaselineConfig
	if err := json.NewDecoder(file).Decode(&config); err != nil {
		return dtos.BaselineConfig{}, ErrDecodeJson
	}
	return config, nil
}

func (s *InitDBService) InitializeDB() error {
	// Load the configuration data
	configData, err := s.LoadConfig()
	if err != nil {
		return err
	}

	// Convert NetworkTechnologies to a list of maps
	technologiesAsMaps, err := mappers.ConvertSliceToMaps(configData.NetworkTechnologies)
	if err != nil {
		return fmt.Errorf("error converting network technologies: %w", err)
	}

	// Debug: Print the list of maps
	for _, techMap := range technologiesAsMaps {
		fmt.Printf("Technology: %+v\n", techMap)
	}

	// Continue with database initialization

	return nil
}
