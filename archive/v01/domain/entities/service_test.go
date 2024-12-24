package entities

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestServiceEntity(t *testing.T) {
	service := &Service{
		ID:          1,
		Name:        "Voice 2G",
		ServiceType: "Voice",
		Technology:  "2G",
		Description: "Standard voice service for 2G",
		RatingID:    1,
	}

	assert.NotNil(t, service)
	assert.Equal(t, 1, service.ID)
	assert.Equal(t, "Voice 2G", service.Name)
	assert.Equal(t, "Voice", service.ServiceType)
	assert.Equal(t, "2G", service.Technology)
	assert.Equal(t, "Standard voice service for 2G", service.Description)
	assert.Equal(t, 1, service.RatingID)
}
