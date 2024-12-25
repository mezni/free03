package bolt_test

import (
	"testing"
	"github.com/stretchr/testify/assert"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/bolt"
	"os"
)

func setupDB() (*bolt.BoltDBLocationRepository, error) {
	// Create a temporary file for the BoltDB database
	dbName := "test.db"
	// Ensure the test db file is cleaned up
	if _, err := os.Stat(dbName); err == nil {
		os.Remove(dbName)
	}

	// Initialize the repository with the test db
	repo, err := bolt.NewBoltDBLocationRepository(dbName)
	if err != nil {
		return nil, err
	}

	return repo, nil
}

func TestCreateLocation(t *testing.T) {
	repo, err := setupDB()
	assert.NoError(t, err)
	defer repo.Close()

	// Create a new location
	location, _ := entities.NewLocation(1, entities.NetworkType2G, "Location1", 10.0, 20.0, 30.0, 40.0)
	err = repo.Create(location)

	// Test if the location was successfully created
	assert.NoError(t, err)

	// Retrieve the location
	locations, err := repo.GetAll()
	assert.NoError(t, err)
	assert.Len(t, locations, 1)
	assert.Equal(t, locations[0].LocationID, 1)
}

func TestCreateMultipleLocations(t *testing.T) {
	repo, err := setupDB()
	assert.NoError(t, err)
	defer repo.Close()

	// Create multiple locations
	location1, _ := entities.NewLocation(1, entities.NetworkType2G, "Location1", 10.0, 20.0, 30.0, 40.0)
	location2, _ := entities.NewLocation(2, entities.NetworkType3G, "Location2", 15.0, 25.0, 35.0, 45.0)

	err = repo.CreateMultiple([]*entities.Location{location1, location2})
	assert.NoError(t, err)

	// Retrieve all locations
	locations, err := repo.GetAll()
	assert.NoError(t, err)
	assert.Len(t, locations, 2)
}

func TestGetRandomLocationByNetworkType(t *testing.T) {
	repo, err := setupDB()
	assert.NoError(t, err)
	defer repo.Close()

	// Create multiple locations
	location1, _ := entities.NewLocation(1, entities.NetworkType2G, "Location1", 10.0, 20.0, 30.0, 40.0)
	location2, _ := entities.NewLocation(2, entities.NetworkType3G, "Location2", 15.0, 25.0, 35.0, 45.0)
	location3, _ := entities.NewLocation(3, entities.NetworkType2G, "Location3", 20.0, 30.0, 40.0, 50.0)

	err = repo.CreateMultiple([]*entities.Location{location1, location2, location3})
	assert.NoError(t, err)

	// Retrieve a random location of network type 2G
	randomLocation, err := repo.GetRandomByNetworkType(entities.NetworkType2G)
	assert.NoError(t, err)
	assert.Contains(t, []int{location1.LocationID, location3.LocationID}, randomLocation.LocationID)

	// Test no locations found for a network type
	randomLocation, err = repo.GetRandomByNetworkType(entities.NetworkType4G)
	assert.Error(t, err)
	assert.Nil(t, randomLocation)
}
