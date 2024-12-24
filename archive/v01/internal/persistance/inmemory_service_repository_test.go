package persistance

import (
	"github.com/mezni/wovoka/domain/entities"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestInMemoryServiceRepository_Create(t *testing.T) {
	repo := NewInMemoryServiceRepository()
	service := &entities.Service{
		ID:          1,
		Name:        "Voice 2G",
		ServiceType: "Voice",
		Technology:  "2G",
		Description: "Standard voice service for 2G",
		RatingID:    1,
	}

	// Create service
	err := repo.Create(service)
	assert.NoError(t, err)

	// Try creating the same service again (should return error)
	err = repo.Create(service)
	assert.Error(t, err)
}

func TestInMemoryServiceRepository_GetByID(t *testing.T) {
	repo := NewInMemoryServiceRepository()
	service := &entities.Service{
		ID:          1,
		Name:        "Voice 2G",
		ServiceType: "Voice",
		Technology:  "2G",
		Description: "Standard voice service for 2G",
		RatingID:    1,
	}

	// Add the service
	repo.Create(service)

	// Get by ID
	foundService, err := repo.GetByID(1)
	assert.NoError(t, err)
	assert.Equal(t, "Voice 2G", foundService.Name)

	// Try getting a non-existing service
	_, err = repo.GetByID(999)
	assert.Error(t, err)
}

func TestInMemoryServiceRepository_List(t *testing.T) {
	repo := NewInMemoryServiceRepository()
	service1 := &entities.Service{
		ID:          1,
		Name:        "Voice 2G",
		ServiceType: "Voice",
		Technology:  "2G",
		Description: "Standard voice service for 2G",
		RatingID:    1,
	}
	service2 := &entities.Service{
		ID:          2,
		Name:        "SMS 2G",
		ServiceType: "Messaging",
		Technology:  "2G",
		Description: "Short Message Service for 2G",
		RatingID:    2,
	}

	// Add services
	repo.Create(service1)
	repo.Create(service2)

	// List all services
	services, err := repo.List()
	assert.NoError(t, err)
	assert.Equal(t, 2, len(services))
}
