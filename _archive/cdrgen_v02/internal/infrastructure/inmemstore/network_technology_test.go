package inmemstore_test

import (
	"github.com/mezni/wovoka/cdrgen/internal/domain/entities"
	"github.com/mezni/wovoka/cdrgen/internal/infrastructure/inmemstore"
	"github.com/stretchr/testify/assert"
	"testing"
)

// TestNetworkTechnologyInMemoryRepository tests the in-memory repository methods
func TestNetworkTechnologyInMemoryRepository(t *testing.T) {
	// Create the in-memory repository instance
	repo := inmemstore.NewNetworkTechnologyInMemoryRepository()

	t.Run("Save and FindByID", func(t *testing.T) {
		// Prepare test data
		networkTechnology := entities.NetworkTechnology{
			ID:   "1",
			Name: "5G",
		}

		// Save the network technology
		err := repo.Save(networkTechnology)
		assert.NoError(t, err)

		// Retrieve the network technology by ID
		storedNetworkTechnology, err := repo.FindByID("1")
		assert.NoError(t, err)
		assert.Equal(t, networkTechnology.ID, storedNetworkTechnology.ID)
		assert.Equal(t, networkTechnology.Name, storedNetworkTechnology.Name)
	})

	t.Run("FindAll", func(t *testing.T) {
		// Prepare test data
		networkTechnologies := []entities.NetworkTechnology{
			{ID: "1", Name: "4G"},
			{ID: "2", Name: "5G"},
		}

		// Save the network technologies
		for _, tech := range networkTechnologies {
			err := repo.Save(tech)
			assert.NoError(t, err)
		}

		// Retrieve all network technologies
		technologies, err := repo.FindAll()
		assert.NoError(t, err)
		assert.Len(t, technologies, 2)
	})

	t.Run("Delete", func(t *testing.T) {
		// Prepare test data
		networkTechnology := entities.NetworkTechnology{
			ID:   "1",
			Name: "4G",
		}

		// Save the network technology
		err := repo.Save(networkTechnology)
		assert.NoError(t, err)

		// Delete the network technology
		err = repo.Delete("1")
		assert.NoError(t, err)

		// Try to find the deleted network technology
		_, err = repo.FindByID("1")
		assert.Error(t, err) // Expect error because it was deleted
	})

	t.Run("FindByID_NotFound", func(t *testing.T) {
		// Try to find a network technology that does not exist
		_, err := repo.FindByID("non-existent-id")
		assert.Error(t, err) // Expect error because it doesn't exist
	})

	t.Run("Delete_NotFound", func(t *testing.T) {
		// Try to delete a network technology that does not exist
		err := repo.Delete("non-existent-id")
		assert.Error(t, err) // Expect error because it doesn't exist
	})
}
