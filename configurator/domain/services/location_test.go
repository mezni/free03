package services

import (
	"github.com/mezni/wovoka/configurator/domain/entities"
	"github.com/mezni/wovoka/configurator/domain/repositories"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
	"testing"
)

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

func (m *MockLocationRepository) GetRandomByNetworkType(networkType entities.NetworkType) (*entities.Location, error) {
	args := m.Called(networkType)
	return args.Get(0).(*entities.Location), args.Error(1)
}

func TestGenerateLocations(t *testing.T) {
	// Create mock repository
	mockRepo := new(MockLocationRepository)

	// Sample config data to test with
	config := CountryConfig{
		Country: "TestCountry",
		Latitude: [2]float64{34.0, 36.0},
		Longitude: [2]float64{-118.0, -116.0},
		Networks: map[string]NetworkConfig{
			"4G": {
				Rows:          2,
				Columns:       2,
				LocationNames: []string{"Downtown", "Uptown"},
			},
		},
	}

	// Create the service instance
	locationService := &LocationService{
		config:     config,
		repository: mockRepo,
	}

	// Define the expected location for mocking
	expectedLocation, err := entities.NewLocation(
		1, 
		entities.NetworkType4G, 
		"Downtown", 
		34.0, 35.0, 
		-118.0, -117.0,
	)
	assert.NoError(t, err)

	// Mock the repository call to create a location
	mockRepo.On("Create", mock.AnythingOfType("*entities.Location")).Return(nil).Once()

	// Mocking GetRandomByNetworkType response
	mockRepo.On("GetRandomByNetworkType", entities.NetworkType4G).Return(expectedLocation, nil)

	// Test location generation
	locations, err := locationService.GenerateLocations()

	// Assert no error occurred
	assert.NoError(t, err)

	// Assert that 4 locations were generated (based on Rows * Columns)
	assert.Len(t, locations, 4)

	// Validate the mock call was made
	mockRepo.AssertExpectations(t)
}

func TestLoadConfig_InvalidFile(t *testing.T) {
	// Test case for loading invalid config file
	_, err := NewLocationService("invalid_file_path.json", nil)
	assert.Error(t, err, "expected an error when loading an invalid config file")
}

func TestGenerateLocations_InvalidConfig(t *testing.T) {
	// Simulating invalid config (empty latitude or longitude range)
	invalidConfig := CountryConfig{
		Country:  "TestCountry",
		Latitude: [2]float64{36.0, 34.0}, // Invalid range
		Longitude: [2]float64{-118.0, -116.0},
		Networks: map[string]NetworkConfig{
			"4G": {
				Rows:          2,
				Columns:       2,
				LocationNames: []string{"Downtown", "Uptown"},
			},
		},
	}

	// Create the service with invalid config
	locationService := &LocationService{
		config:     invalidConfig,
		repository: nil, // No repository needed for this test
	}

	// Test that the service fails when generating locations due to invalid config
	locations, err := locationService.GenerateLocations()
	assert.Error(t, err)
	assert.Nil(t, locations, "expected nil locations due to invalid config")
}
