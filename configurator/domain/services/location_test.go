package services

import (
	"github.com/mezni/wovoka/configurator/domain/entities"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"testing"
)

// MockLocationRepository is a mock implementation of the LocationRepository interface
type MockLocationRepository struct {
	mock.Mock
}

func (m *MockLocationRepository) Create(location *entities.Location) error {
	args := m.Called(location)
	return args.Error(0)
}

func (m *MockLocationRepository) GetByID(id int) (*entities.Location, error) {
	args := m.Called(id)
	return args.Get(0).(*entities.Location), args.Error(1)
}

func (m *MockLocationRepository) Update(location *entities.Location) error {
	args := m.Called(location)
	return args.Error(0)
}

func (m *MockLocationRepository) Delete(id int) error {
	args := m.Called(id)
	return args.Error(0)
}

func (m *MockLocationRepository) GetAll() ([]*entities.Location, error) {
	args := m.Called()
	return args.Get(0).([]*entities.Location), args.Error(1)
}

func TestGenerateLocations(t *testing.T) {
	// Define the mock repository
	mockRepo := new(MockLocationRepository)

	// Sample configuration for testing
	config := CountryConfig{
		Country:   "Tunisia",
		Latitude:  [2]float64{30.24, 37.54},
		Longitude: [2]float64{7.52, 11.60},
		Networks: map[string]NetworkConfig{
			"2G": {
				Rows:          3,
				Columns:       1,
				LocationNames: []string{"nord", "centre", "centre"},
			},
			"3G": {
				Rows:          3,
				Columns:       1,
				LocationNames: []string{"nord", "centre", "centre"},
			},
		},
	}

	// Create the service instance with the mock repository
	service := &LocationService{
		config:     config,
		repository: mockRepo,
	}

	// Set up expectations for the mock repository
	mockRepo.On("Create", mock.Anything).Return(nil).Times(6)

	// Call GenerateLocations method
	locations, err := service.GenerateLocations()

	// Assert that there are no errors
	assert.NoError(t, err)

	// Assert that 6 locations are generated
	assert.Len(t, locations, 6)

	// Assert that Create method was called 6 times
	mockRepo.AssertExpectations(t)

	// Optionally, verify the properties of the generated locations
	for i, location := range locations {
		// Check if location name is correct based on the index (cyclic behavior)
		expectedLocationName := config.Networks["2G"].LocationNames[(i)%len(config.Networks["2G"].LocationNames)]
		assert.Equal(t, expectedLocationName, location.LocationName)

		// Ensure latitude and longitude are within bounds
		assert.Greater(t, location.LatMin, 0.0)
		assert.Less(t, location.LatMax, 40.0)
		assert.Greater(t, location.LonMin, 0.0)
		assert.Less(t, location.LonMax, 20.0)
	}
}
