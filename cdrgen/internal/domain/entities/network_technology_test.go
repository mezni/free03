package entities_test

import (
	"testing"
	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
	"github.com/mezni/wovoka/cdrgen/internal/domain/entities"
)

func TestNetworkTechnologyFactory_NewNetworkTechnology(t *testing.T) {
	factory := &entities.NetworkTechnologyFactory{}

	// Create a new NetworkTechnology
	nt := factory.NewNetworkTechnology("6G", "Sixth Generation Cellular Network")

	// Assert that the ID is a valid UUID
	_, err := uuid.Parse(nt.ID)
	assert.NoError(t, err, "ID should be a valid UUID")

	// Assert the Name and Description are correct
	assert.Equal(t, "6G", nt.Name)
	assert.Equal(t, "Sixth Generation Cellular Network", nt.Description)
}

func TestPredefinedNetworkTechnologies(t *testing.T) {
	factory := &entities.NetworkTechnologyFactory{}
	technologies := entities.PredefinedNetworkTechnologies(factory)

	// Assert that the length of predefined technologies is 4
	assert.Equal(t, 4, len(technologies))

	// Assert the expected names and descriptions for each technology
	assert.Equal(t, "2G", technologies[0].Name)
	assert.Equal(t, "Second Generation Cellular Network", technologies[0].Description)

	assert.Equal(t, "3G", technologies[1].Name)
	assert.Equal(t, "Third Generation Cellular Network", technologies[1].Description)

	assert.Equal(t, "4G", technologies[2].Name)
	assert.Equal(t, "Fourth Generation Cellular Network", technologies[2].Description)

	assert.Equal(t, "5G", technologies[3].Name)
	assert.Equal(t, "Fifth Generation Cellular Network", technologies[3].Description)
}

func TestNetworkTechnologyFactory_UniqueID(t *testing.T) {
	factory := &entities.NetworkTechnologyFactory{}

	// Create two NetworkTechnology instances
	nt1 := factory.NewNetworkTechnology("6G", "Sixth Generation Cellular Network")
	nt2 := factory.NewNetworkTechnology("7G", "Seventh Generation Cellular Network")

	// Assert that the IDs are unique
	assert.NotEqual(t, nt1.ID, nt2.ID, "IDs should be unique")
}

func TestPredefinedNetworkTechnologies_IDsAreUnique(t *testing.T) {
	factory := &entities.NetworkTechnologyFactory{}
	technologies := entities.PredefinedNetworkTechnologies(factory)

	// Collect the IDs of the predefined technologies
	ids := make(map[string]bool)
	for _, nt := range technologies {
		ids[nt.ID] = true
	}

	// Assert that the number of unique IDs matches the number of technologies
	assert.Equal(t, len(ids), len(technologies), "All predefined technologies should have unique IDs")
}
