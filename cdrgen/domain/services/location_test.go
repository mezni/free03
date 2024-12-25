package services_test

import (
	"encoding/json"
	"fmt"
	"os"
	"testing"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/domain/services"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmem"
	"github.com/stretchr/testify/assert"
)

func TestGenerateLocations(t *testing.T) {
	// Create an in-memory location repository
	repo := inmem.NewInMemoryLocationRepository()

	// Create the test configuration
	config := services.CountryConfig{
		Country: "TestCountry",
		Coordinates: services.Coordinates{
			Latitude:  [2]float64{10.0, 20.0},
			Longitude: [2]float64{-50.0, -40.0},
		},
		Networks: map[string]services.NetworkConfig{
			"2G": {Rows: 2, Columns: 2, LocationNames: []string{"SiteA", "SiteB"}},
			"3G": {Rows: 2, Columns: 2, LocationNames: []string{"SiteC", "SiteD"}},
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
	assert.Len(t, locations, 8) // 2 networks (2G, 3G) with a 2x2 grid for each (2 * 2 * 2)

	// Test retrieval of all locations
	allLocations, err := service.GetAllLocations()
	assert.NoError(t, err)
	assert.Len(t, allLocations, 8)

	// Test retrieval of a random location by network type (2G)
	randomLocation2G, err := service.GetRandomLocationByNetworkType(entities.NetworkType2G)
	assert.NoError(t, err)
	assert.Contains(t, []int{locations[0].LocationID, locations[1].LocationID, locations[2].LocationID, locations[3].LocationID}, randomLocation2G.LocationID)

	// Test retrieval of a random location by network type (3G)
	randomLocation3G, err := service.GetRandomLocationByNetworkType(entities.NetworkType3G)
	assert.NoError(t, err)
	assert.Contains(t, []int{locations[4].LocationID, locations[5].LocationID, locations[6].LocationID, locations[7].LocationID}, randomLocation3G.LocationID)
}

func TestGenerateAreaCode(t *testing.T) {
	// Create an in-memory location repository
	repo := inmem.NewInMemoryLocationRepository()

	// Create the test configuration
	config := services.CountryConfig{
		Country: "TestCountry",
		Coordinates: services.Coordinates{
			Latitude:  [2]float64{10.0, 20.0},
			Longitude: [2]float64{-50.0, -40.0},
		},
		Networks: map[string]services.NetworkConfig{
			"2G": {Rows: 1, Columns: 1, LocationNames: []string{"SiteA"}},
		},
	}

	// Write the configuration to a temporary file
	configFile, err := os.CreateTemp("", "test_config_*.json")
	if err != nil {
		t.Fatalf("Error creating temp config file: %v", err)
	}
	defer os.Remove(configFile.Name())

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

	// Test AreaCode generation for 2G network type
	areaCode2G, err := service.GenerateAreaCode(entities.NetworkType2G)
	assert.NoError(t, err)
	assert.Equal(t, 4, len(fmt.Sprintf("%d", areaCode2G)), "AreaCode should have a length of 4 digits")

	// Test AreaCode generation for 3G network type
	areaCode3G, err := service.GenerateAreaCode(entities.NetworkType3G)
	assert.NoError(t, err)
	assert.Equal(t, 4, len(fmt.Sprintf("%d", areaCode3G)), "AreaCode should have a length of 4 digits")

	// Test AreaCode generation for 4G network type
	areaCode4G, err := service.GenerateAreaCode(entities.NetworkType4G)
	assert.NoError(t, err)
	assert.Equal(t, 4, len(fmt.Sprintf("%d", areaCode4G)), "AreaCode should have a length of 4 digits")

	// Test AreaCode generation for 5G network type
	areaCode5G, err := service.GenerateAreaCode(entities.NetworkType5G)
	assert.NoError(t, err)
	assert.Equal(t, 4, len(fmt.Sprintf("%d", areaCode5G)), "AreaCode should have a length of 4 digits")
}
