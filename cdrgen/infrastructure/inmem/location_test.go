package inmem_test

import (
	"testing"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmem"
	"github.com/stretchr/testify/assert"
)

func TestCreateLocation(t *testing.T) {
	repo := inmem.NewInMemoryLocationRepository()

	// Create a new location
	location, _ := entities.NewLocation(1, entities.NetworkType2G, "Location1", 10.0, 20.0, 30.0, 40.0, 1234)
	err := repo.Create(location)

	// Test if the location was successfully created
	assert.NoError(t, err)
	assert.Equal(t, 1234, location.AreaCode)

	// Test that creating a location with the same ID fails
	err = repo.Create(location)
	assert.Error(t, err)
}

func TestCreateMultipleLocations(t *testing.T) {
	repo := inmem.NewInMemoryLocationRepository()

	// Create new locations
	location1, _ := entities.NewLocation(1, entities.NetworkType2G, "Location1", 10.0, 20.0, 30.0, 40.0, 1234)
	location2, _ := entities.NewLocation(2, entities.NetworkType3G, "Location2", 15.0, 25.0, 35.0, 45.0, 5678)

	err := repo.CreateMultiple([]*entities.Location{location1, location2})

	// Test if the locations were successfully created
	assert.NoError(t, err)
	assert.Equal(t, 1234, location1.AreaCode)
	assert.Equal(t, 5678, location2.AreaCode)

	// Try creating multiple locations again with one existing location
	err = repo.CreateMultiple([]*entities.Location{location1, location2})
	assert.Error(t, err)
}

func TestGetAllLocations(t *testing.T) {
	repo := inmem.NewInMemoryLocationRepository()

	// Create new locations
	location1, _ := entities.NewLocation(1, entities.NetworkType2G, "Location1", 10.0, 20.0, 30.0, 40.0, 1234)
	location2, _ := entities.NewLocation(2, entities.NetworkType3G, "Location2", 15.0, 25.0, 35.0, 45.0, 5678)

	repo.CreateMultiple([]*entities.Location{location1, location2})

	locations, err := repo.GetAll()

	// Test if the locations were retrieved successfully
	assert.NoError(t, err)
	assert.Len(t, locations, 2)
	assert.Equal(t, 1234, locations[0].AreaCode)
	assert.Equal(t, 5678, locations[1].AreaCode)
}

func TestGetRandomLocationByNetworkType(t *testing.T) {
	repo := inmem.NewInMemoryLocationRepository()

	// Create new locations
	location1, _ := entities.NewLocation(1, entities.NetworkType2G, "Location1", 10.0, 20.0, 30.0, 40.0, 1234)
	location2, _ := entities.NewLocation(2, entities.NetworkType3G, "Location2", 15.0, 25.0, 35.0, 45.0, 5678)
	location3, _ := entities.NewLocation(3, entities.NetworkType2G, "Location3", 20.0, 30.0, 40.0, 50.0, 9101)

	repo.CreateMultiple([]*entities.Location{location1, location2, location3})

	randomLocation, err := repo.GetRandomByNetworkType(entities.NetworkType2G)

	// Test if the random location was retrieved successfully
	assert.NoError(t, err)
	assert.Contains(t, []int{location1.LocationID, location3.LocationID}, randomLocation.LocationID)

	// Test no locations found for a network type
	randomLocation, err = repo.GetRandomByNetworkType(entities.NetworkType4G)
	assert.Error(t, err)
	assert.Nil(t, randomLocation)
}
