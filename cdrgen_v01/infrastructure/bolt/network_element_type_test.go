package bolt_test

import (
	"testing"
	"github.com/mezni/wovoka/cdrgen/infrastructure/bolt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"os"
)

func TestBoltNetworkElementRepo_Create(t *testing.T) {
	// Create a temporary file for the database
	dbFilePath := "./test.db"
	defer os.Remove(dbFilePath)

	repo, err := bolt.NewBoltNetworkElementRepo(dbFilePath)
	require.NoError(t, err)
	defer repo.DB.Close() // Ensure the DB is closed after the test

	// Create a new NetworkElement
	desc := "Sample description"
	ne, err := entities.NewNetworkElement(1, entities.NetworkType4G, "Element1", &desc)
	require.NoError(t, err)

	// Add the NetworkElement to the repository
	err = repo.Create(ne)
	require.NoError(t, err)

	// Check if the element is successfully stored
	elements, err := repo.GetAll()
	require.NoError(t, err)
	assert.Len(t, elements, 1)
	assert.Equal(t, ne, elements[0])
}

func TestBoltNetworkElementRepo_CreateMultiple(t *testing.T) {
	// Create a temporary file for the database
	dbFilePath := "./test.db"
	defer os.Remove(dbFilePath)

	repo, err := bolt.NewBoltNetworkElementRepo(dbFilePath)
	require.NoError(t, err)
	defer repo.DB.Close()

	// Create multiple NetworkElements
	desc1 := "Description 1"
	ne1, err := entities.NewNetworkElement(1, entities.NetworkType4G, "Element1", &desc1)
	require.NoError(t, err)

	desc2 := "Description 2"
	ne2, err := entities.NewNetworkElement(2, entities.NetworkType5G, "Element2", &desc2)
	require.NoError(t, err)

	// Add multiple elements
	err = repo.CreateMultiple([]*entities.NetworkElement{ne1, ne2})
	require.NoError(t, err)

	// Check if both elements are added
	elements, err := repo.GetAll()
	require.NoError(t, err)
	assert.Len(t, elements, 2)
	assert.Contains(t, elements, ne1)
	assert.Contains(t, elements, ne2)
}

func TestBoltNetworkElementRepo_GetRandomByNetworkType(t *testing.T) {
	// Create a temporary file for the database
	dbFilePath := "./test.db"
	defer os.Remove(dbFilePath)

	repo, err := bolt.NewBoltNetworkElementRepo(dbFilePath)
	require.NoError(t, err)
	defer repo.DB.Close()

	// Create NetworkElements with different types
	desc1 := "Description 1"
	ne1, err := entities.NewNetworkElement(1, entities.NetworkType4G, "Element1", &desc1)
	require.NoError(t, err)

	desc2 := "Description 2"
	ne2, err := entities.NewNetworkElement(2, entities.NetworkType5G, "Element2", &desc2)
	require.NoError(t, err)

	// Add elements to the repository
	err = repo.CreateMultiple([]*entities.NetworkElement{ne1, ne2})
	require.NoError(t, err)

	// Get a random element of NetworkType4G
	randomElement, err := repo.GetRandomByNetworkType(entities.NetworkType4G)
	require.NoError(t, err)
	assert.Equal(t, ne1, randomElement)

	// Get a random element of NetworkType5G
	randomElement, err = repo.GetRandomByNetworkType(entities.NetworkType5G)
	require.NoError(t, err)
	assert.Equal(t, ne2, randomElement)

	// Try to get a random element of a non-existent network type (2G)
	randomElement, err = repo.GetRandomByNetworkType(entities.NetworkType2G)
	assert.Error(t, err)
	assert.Nil(t, randomElement)
}
