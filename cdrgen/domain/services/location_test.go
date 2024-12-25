package services_test

import (
	"encoding/json"
	"os"
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmem" 
	"github.com/mezni/wovoka/cdrgen/domain/services"
)

func TestGenerateLocations(t *testing.T) {
	// Create an in-memory location repository
	repo := inmem.NewInMemoryLocationRepository()

	// Create the test configuration
	config := services.CountryConfig{
		Country:  "TestCountry",
		Latitude: [2]float64{10.0, 20.0},
		Longitude: [2]float64{-50.0, -40.0},
		Networks: map[string]services.NetworkConfig{
			"2G": {Rows: 2, Columns: 2, LocationNames: []string{"SiteA", "SiteB"}},
		},
	}

	// Write the configuration to a temporary file
	configFile, err := os.CreateTemp("", "test_config_*.json")
	if err != nil {
		t.Fatalf("Error creating temp config file: %v", err)
	}
	defer os.Remove(configFile.Name()) // Clean up the temp file after the test

	// Encode the configuration to the file
	encoder := json.NewEncoder(configFile)
	err = encoder.Encode(config)
	if err != nil {
		t.Fatalf("Error encoding config to temp file: %v", err)
	}

	// Reopen the file for the LocationService constructor
	configFile.Close()

	// Initialize the LocationService using the temp config file
	service, err := services.NewLocationService(configFile.Name(), repo)
	assert.NoError(t, err)

	// Generate locations
	locations, err := service.GenerateLocations()
	assert.NoError(t, err)
	assert.Len(t, locations, 4) // Based on the grid size (2x2)

	// Test retrieval of all locations
	allLocations, err := service.GetAllLocations()
	assert.NoError(t, err)
	assert.Len(t, allLocations, 4)

	// Test retrieval of a random location by network type
	randomLocation, err := service.GetRandomLocationByNetworkType(entities.NetworkType2G)
	assert.NoError(t, err)
	assert.Contains(t, []int{locations[0].LocationID, locations[1].LocationID, locations[2].LocationID, locations[3].LocationID}, randomLocation.LocationID)
}