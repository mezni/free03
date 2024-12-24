package entities

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestNewLocation(t *testing.T) {
	// Test valid location creation
	location, err := NewLocation(1, NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	assert.NoError(t, err)
	assert.NotNil(t, location)
	assert.Equal(t, 1, location.LocationID)
	assert.Equal(t, "Downtown", location.LocationName)
	assert.Equal(t, NetworkType4G, location.NetworkType)
	assert.Equal(t, 40.7128, location.Latitude)
	assert.Equal(t, 40.9152, location.LatitudeMax)
	assert.Equal(t, -74.0060, location.Longitude)
	assert.Equal(t, -73.7004, location.LongitudeMax)

	// Test invalid network type (should return an error)
	_, err = NewLocation(2, "InvalidNetworkType", "Uptown", 40.7308, 40.7552, -74.0000, -73.6800)
	assert.Error(t, err)
	assert.Equal(t, "invalid network type", err.Error())
}

func TestLocation_Validate(t *testing.T) {
	// Test valid location validation
	location, err := NewLocation(1, NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	assert.NoError(t, err)
	err = location.Validate()
	assert.NoError(t, err)

	// Test invalid location (missing network type)
	invalidLocation := &Location{
		LocationID:   2,
		LocationName: "Uptown",
		NetworkType:  "",
		Latitude:     40.7308,
		Longitude:    -74.0000,
	}
	err = invalidLocation.Validate()
	assert.Error(t, err)
	assert.Equal(t, "network type cannot be empty", err.Error())

	// Test invalid location (latitude out of range)
	invalidLocation = &Location{
		LocationID:   3,
		LocationName: "Invalid Location",
		NetworkType:  NetworkType4G,
		Latitude:     100.0, // Invalid latitude
		Longitude:    -74.0000,
	}
	err = invalidLocation.Validate()
	assert.Error(t, err)
	assert.Equal(t, "latitude must be between -90 and 90", err.Error())

	// Test invalid location (longitude out of range)
	invalidLocation = &Location{
		LocationID:   4,
		LocationName: "Invalid Location",
		NetworkType:  NetworkType4G,
		Latitude:     40.7308,
		Longitude:    200.0, // Invalid longitude
	}
	err = invalidLocation.Validate()
	assert.Error(t, err)
	assert.Equal(t, "longitude must be between -180 and 180", err.Error())
}

func TestLocation_Equality(t *testing.T) {
	location1, err := NewLocation(1, NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	assert.NoError(t, err)
	location2, err := NewLocation(1, NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	assert.NoError(t, err)
	location3, err := NewLocation(2, NetworkType5G, "Uptown", 40.7308, 40.7552, -74.0000, -73.6800)
	assert.NoError(t, err)

	// Test equality for two identical locations
	assert.True(t, location1.Equals(location2))

	// Test inequality for different locations
	assert.False(t, location1.Equals(location3))
}

func TestLocation_Setters(t *testing.T) {
	location, err := NewLocation(1, NetworkType4G, "Downtown", 40.7128, 40.9152, -74.0060, -73.7004)
	assert.NoError(t, err)

	// Test updating the name
	location.SetLocationName("Uptown")
	assert.Equal(t, "Uptown", location.LocationName)

	// Test updating the latitude
	location.SetLatitude(41.0)
	assert.Equal(t, 41.0, location.Latitude)

	// Test updating the longitude
	location.SetLongitude(-75.0)
	assert.Equal(t, -75.0, location.Longitude)

	// Test updating the network type
	location.SetNetworkType(NetworkType5G)
	assert.Equal(t, NetworkType5G, location.NetworkType)
}
