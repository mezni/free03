package services

import (
	"os"
	"testing"
	//	"github.com/mezni/wovoka/domain/entities"
	"github.com/stretchr/testify/assert"
)

func TestLoadServicesFromFile(t *testing.T) {
	// Create a test file with sample JSON data
	fileContent := `[
		{"ID": 1, "Name": "Voice 2G", "ServiceType": "Voice", "Technology": "2G", "Description": "Standard voice service for 2G", "RatingID": 1},
		{"ID": 2, "Name": "SMS 2G", "ServiceType": "Messaging", "Technology": "2G", "Description": "Short Message Service for 2G", "RatingID": 2}
	]`
	err := os.WriteFile("test_services.json", []byte(fileContent), 0644)
	assert.NoError(t, err)
	defer os.Remove("test_services.json")

	// Create an instance of ServiceService
	serviceService := NewServiceService(nil)

	// Test loading services from the file
	services, err := serviceService.LoadServicesFromFile("test_services.json")
	assert.NoError(t, err)
	assert.Equal(t, 2, len(services))
	assert.Equal(t, "Voice 2G", services[0].Name)
	assert.Equal(t, "SMS 2G", services[1].Name)
}
