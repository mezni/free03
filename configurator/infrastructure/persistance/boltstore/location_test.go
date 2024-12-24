package boltstore

import (
	"github.com/mezni/wovoka/configurator/domain/entities"
	"github.com/stretchr/testify/assert"
	"testing"
)

func createTestRepository(t *testing.T) (*BoltDBLocationRepository, func()) {
	// Create a temporary test DB file
	dbFile := "test_locations.db"
	repo, err := NewBoltDBLocationRepository(dbFile)
	if err != nil {
		t.Fatalf("Failed to create repository: %v", err)
	}

	// Clean up after the test by deleting the DB file
	return repo, func() {
		repo.db.Close()
		// Clean up the test database file
		// Note: Do not rely on this in production tests as it may leave files behind on failure
	}
}

func TestCreateLocation(t *testing.T) {
	repo, cleanup := createTestRepository(t)
	defer cleanup()

	location, err := entities.NewLocation(1, entities.NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	assert.NoError(t, err)

	// Test creating a new location
	err = repo.Create(location)
	assert.NoError(t, err)

	// Try to create the same location again (should fail)
	err = repo.Create(location)
	assert.Error(t, err)
}

func TestGetByID(t *testing.T) {
	repo, cleanup := createTestRepository(t)
	defer cleanup()

	location, err := entities.NewLocation(1, entities.NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	assert.NoError(t, err)

	err = repo.Create(location)
	assert.NoError(t, err)

	// Test retrieving the location by ID
	retrievedLocation, err := repo.GetByID(1)
	assert.NoError(t, err)
	assert.NotNil(t, retrievedLocation)
	assert.Equal(t, location.LocationID, retrievedLocation.LocationID)

	// Test getting a non-existent location
	_, err = repo.GetByID(999)
	assert.Error(t, err)
}

func TestUpdateLocation(t *testing.T) {
	repo, cleanup := createTestRepository(t)
	defer cleanup()

	location, err := entities.NewLocation(1, entities.NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	assert.NoError(t, err)

	err = repo.Create(location)
	assert.NoError(t, err)

	// Update the location's name
	location.LocationName = "Uptown"
	err = repo.Update(location)
	assert.NoError(t, err)

	// Retrieve the updated location
	retrievedLocation, err := repo.GetByID(1)
	assert.NoError(t, err)
	assert.Equal(t, "Uptown", retrievedLocation.LocationName)

	// Try to update a non-existent location
	nonExistentLocation := &entities.Location{LocationID: 999}
	err = repo.Update(nonExistentLocation)
	assert.Error(t, err)
}

func TestDeleteLocation(t *testing.T) {
	repo, cleanup := createTestRepository(t)
	defer cleanup()

	location, err := entities.NewLocation(1, entities.NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	assert.NoError(t, err)

	err = repo.Create(location)
	assert.NoError(t, err)

	// Delete the location
	err = repo.Delete(1)
	assert.NoError(t, err)

	// Try to retrieve the deleted location
	_, err = repo.GetByID(1)
	assert.Error(t, err)
}

func TestGetAllLocations(t *testing.T) {
	repo, cleanup := createTestRepository(t)
	defer cleanup()

	location1, err := entities.NewLocation(1, entities.NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	assert.NoError(t, err)
	location2, err := entities.NewLocation(2, entities.NetworkType5G, "Uptown", 40.7308, 40.7552, -74.0000, -73.6800)
	assert.NoError(t, err)

	err = repo.Create(location1)
	assert.NoError(t, err)
	err = repo.Create(location2)
	assert.NoError(t, err)

	// Retrieve all locations
	allLocations, err := repo.GetAll()
	assert.NoError(t, err)
	assert.Len(t, allLocations, 2)
	assert.Equal(t, "Downtown", allLocations[0].LocationName)
	assert.Equal(t, "Uptown", allLocations[1].LocationName)
}

func TestGetRandomByNetworkType(t *testing.T) {
	repo, cleanup := createTestRepository(t)
	defer cleanup()

	location1, err := entities.NewLocation(1, entities.NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	assert.NoError(t, err)
	location2, err := entities.NewLocation(2, entities.NetworkType4G, "Uptown", 40.7308, 40.7552, -74.0000, -73.6800)
	assert.NoError(t, err)
	location3, err := entities.NewLocation(3, entities.NetworkType5G, "Midtown", 40.7480, 40.7550, -74.0020, -73.6900)
	assert.NoError(t, err)

	err = repo.Create(location1)
	assert.NoError(t, err)
	err = repo.Create(location2)
	assert.NoError(t, err)
	err = repo.Create(location3)
	assert.NoError(t, err)

	// Test GetRandomByNetworkType for 4G
	randomLocation, err := repo.GetRandomByNetworkType(entities.NetworkType4G)
	assert.NoError(t, err)
	assert.True(t, randomLocation.NetworkType == entities.NetworkType4G)

	// Test
