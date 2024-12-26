package boltstore_test

import (
	"os"
	"testing"

	"github.com/boltdb/bolt"
	"github.com/stretchr/testify/assert"

	"github.com/mezni/wovoka/cdrgen/internal/domain/entities"
	"github.com/mezni/wovoka/cdrgen/internal/infrastructure/boltstore"
)

const testBucketName = "TestNetworkTechnologies"

func setupTestDB(t *testing.T) (*bolt.DB, func()) {
	// Create a temporary database file for testing
	db, err := bolt.Open("test.db", 0600, nil)
	if err != nil {
		t.Fatalf("Failed to open BoltDB: %v", err)
	}

	// Return cleanup function
	return db, func() {
		db.Close()
		os.Remove("test.db") // Remove the test database file after the tests
	}
}

func TestNetworkTechnologyBoltDBRepository(t *testing.T) {
	db, cleanup := setupTestDB(t)
	defer cleanup()

	// Initialize the repository
	repo, err := boltstore.NewNetworkTechnologyBoltDBRepository(db, testBucketName)
	assert.NoError(t, err)

	t.Run("Save and FindByID", func(t *testing.T) {
		// Prepare test data
		networkTechnology := entities.NetworkTechnology{
			ID:          "1",
			Name:        "5G",
			Description: "Fifth-generation wireless technology",
		}

		// Save the network technology
		err := repo.Save(networkTechnology)
		assert.NoError(t, err)

		// Retrieve the network technology by ID
		storedNetworkTechnology, err := repo.FindByID("1")
		assert.NoError(t, err)
		assert.Equal(t, networkTechnology.ID, storedNetworkTechnology.ID)
		assert.Equal(t, networkTechnology.Name, storedNetworkTechnology.Name)
		assert.Equal(t, networkTechnology.Description, storedNetworkTechnology.Description)
	})

	t.Run("FindAll", func(t *testing.T) {
		// Prepare test data
		networkTechnologies := []entities.NetworkTechnology{
			{ID: "1", Name: "4G", Description: "Fourth-generation wireless technology"},
			{ID: "2", Name: "5G", Description: "Fifth-generation wireless technology"},
		}

		// Save the network technologies
		for _, tech := range networkTechnologies {
			err := repo.Save(tech)
			assert.NoError(t, err)
		}

		// Retrieve all network technologies
		technologies, err := repo.FindAll()
		assert.NoError(t, err)
		assert.Len(t, technologies, len(networkTechnologies))

		// Verify data matches
		for i, tech := range technologies {
			assert.Equal(t, networkTechnologies[i].ID, tech.ID)
			assert.Equal(t, networkTechnologies[i].Name, tech.Name)
			assert.Equal(t, networkTechnologies[i].Description, tech.Description)
		}
	})

	t.Run("Delete", func(t *testing.T) {
		// Prepare test data
		networkTechnology := entities.NetworkTechnology{
			ID:          "3",
			Name:        "LTE",
			Description: "Long Term Evolution",
		}

		// Save the network technology
		err := repo.Save(networkTechnology)
		assert.NoError(t, err)

		// Delete the network technology
		err = repo.Delete("3")
		assert.NoError(t, err)

		// Try to find the deleted network technology
		_, err = repo.FindByID("3")
		assert.Error(t, err) // Expect error because it was deleted
	})

	t.Run("FindByID_NotFound", func(t *testing.T) {
		// Try to find a network technology that does not exist
		_, err := repo.FindByID("non-existent-id")
		assert.Error(t, err) // Expect error because it doesn't exist
	})
}
