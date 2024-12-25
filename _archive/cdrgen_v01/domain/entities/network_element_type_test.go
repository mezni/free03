package entities_test

import (
	"testing"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/stretchr/testify/assert"
)

func TestNewNetworkElement(t *testing.T) {
	// Valid network element with description
	desc := "5G Base Station"
	ne, err := entities.NewNetworkElement(1, entities.NetworkType5G, "gNodeB", &desc)
	assert.NoError(t, err)
	assert.Equal(t, 1, ne.NetworkElementTypeID)
	assert.Equal(t, entities.NetworkType5G, ne.NetworkType)
	assert.Equal(t, "gNodeB", ne.NetworkElementName)
	assert.Equal(t, "5G Base Station", *ne.NetworkElementDesc)

	// Valid network element without description (nil)
	ne, err = entities.NewNetworkElement(2, entities.NetworkType4G, "eNodeB", nil)
	assert.NoError(t, err)
	assert.Equal(t, 2, ne.NetworkElementTypeID)
	assert.Equal(t, entities.NetworkType4G, ne.NetworkType)
	assert.Equal(t, "eNodeB", ne.NetworkElementName)
	assert.Nil(t, ne.NetworkElementDesc)

	// Invalid network type
	_, err = entities.NewNetworkElement(0, 999, "eNodeB", nil)
	assert.Error(t, err)

	// Invalid empty NetworkElementName
	_, err = entities.NewNetworkElement(2, entities.NetworkType4G, "", nil)
	assert.EqualError(t, err, "NetworkElementName cannot be empty")
}
