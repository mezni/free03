package inmem_test

import (
	"testing"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmem"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestInMemoryNetworkElementRepo_Create(t *testing.T) {
	repo := inmem.NewInMemoryNetworkElementRepo()

	// Create a new NetworkElement
	desc := "Sample description"
	networkElement, err := entities.NewNetworkElement(1, entities.NetworkType4G, "Element1", &desc)
	require.NoError(t, err)

	// Add the NetworkElement to the repository
	err = repo.Create(networkElement)
	require.NoError(t, err)

	// Check if the element is successfully stored
	elements, err := repo.GetAll()
	require.NoError(t, err)
	assert.Len(t, elements, 1)
	assert.Equal(t, networkElement, elements[0])
}

func TestInMemoryNetworkElementRepo_CreateMultiple(t *testing.T) {
	repo := inmem.NewInMemoryNetworkElementRepo()

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

func TestInMemoryNetworkElementRepo_GetAll(t *testing.T) {
	repo := inmem.NewInMemoryNetworkElementRepo()

	// Add NetworkElements
	desc := "Description"
	ne1, err := entities.NewNetworkElement(1, entities.NetworkType4G, "Element1", &desc)
	require.NoError(t, err)

	err = repo.Create(ne1)
	require.NoError(t, err)

	// Fetch all elements
	elements, err := repo.GetAll()
	require.NoError(t, err)
	assert.Len(t, elements, 1)
	assert.Equal(t, ne1, elements[0])
}

func TestInMemoryNetworkElementRepo_GetRandomByNetworkType(t *testing.T) {
	repo := inmem.NewInMemoryNetworkElementRepo()

	// Create NetworkElements with different types
	desc1 := "Description 1"
	ne1, err := entities.NewNetworkElement(1, entities.NetworkType4G, "Element1", &desc1)
	require.NoError(t, err)

	desc2 := "Description 2"
	ne2, err := entities.NewNetworkElement(2, entities.NetworkType5G, "Element2", &desc2)
	require.NoError(t, err)

	err = repo.CreateMultiple([]*entities.NetworkElement{ne1, ne2})
	require.NoError(t, err)

	// Fetch random element by NetworkType (4G)
	randomElement, err := repo.GetRandomByNetworkType(entities.NetworkType4G)
	require.NoError(t, err)
	assert.Equal(t, ne1, randomElement)

	// Fetch random element by NetworkType (5G)
	randomElement, err = repo.GetRandomByNetworkType(entities.NetworkType5G)
	require.NoError(t, err)
	assert.Equal(t, ne2, randomElement)

	// Fetch random element by a non-existing NetworkType (2G)
	randomElement, err = repo.GetRandomByNetworkType(entities.NetworkType2G)
	assert.Error(t, err)
	assert.Nil(t, randomElement)
}
