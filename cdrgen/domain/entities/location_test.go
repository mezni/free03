package entities_test

import (
	"testing"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/stretchr/testify/assert"
)

func TestNewLocation_Valid(t *testing.T) {
	loc, err := entities.NewLocation(1, entities.NetworkType2G, "nord", 30.0, 31.0, 7.0, 8.0, 1234)
	assert.Nil(t, err)
	assert.NotNil(t, loc)
	assert.Equal(t, loc.LocationID, 1)
	assert.Equal(t, loc.NetworkType, entities.NetworkType2G)
	assert.Equal(t, loc.LocationName, "nord")
	assert.Equal(t, loc.LatMin, 30.0)
	assert.Equal(t, loc.LatMax, 31.0)
	assert.Equal(t, loc.LonMin, 7.0)
	assert.Equal(t, loc.LonMax, 8.0)
	assert.Equal(t, loc.AreaCode, 1234)
}

func TestNewLocation_InvalidLatitude(t *testing.T) {
	_, err := entities.NewLocation(1, entities.NetworkType2G, "nord", 95.0, 100.0, 7.0, 8.0, 1234)
	assert.Equal(t, err, entities.ErrInvalidLatitude)
}

func TestNewLocation_InvalidLongitude(t *testing.T) {
	_, err := entities.NewLocation(1, entities.NetworkType2G, "nord", 30.0, 31.0, -200.0, 180.0, 1234)
	assert.Equal(t, err, entities.ErrInvalidLongitude)
}

func TestNewLocation_EmptyLocationName(t *testing.T) {
	_, err := entities.NewLocation(1, entities.NetworkType2G, "", 30.0, 31.0, 7.0, 8.0, 1234)
	assert.Equal(t, err, entities.ErrEmptyLocationName)
}

func TestNewLocation_LatMinGreaterThanLatMax(t *testing.T) {
	_, err := entities.NewLocation(1, entities.NetworkType2G, "nord", 35.0, 30.0, 7.0, 8.0, 1234)
	assert.Equal(t, err, entities.ErrLatitudeOrder)
}

func TestNewLocation_LonMinGreaterThanLonMax(t *testing.T) {
	_, err := entities.NewLocation(1, entities.NetworkType2G, "nord", 30.0, 31.0, 9.0, 8.0, 1234)
	assert.Equal(t, err, entities.ErrLongitudeOrder)
}

func TestNewLocation_InvalidNetworkType(t *testing.T) {
	_, err := entities.NewLocation(1, entities.NetworkType(100), "nord", 30.0, 31.0, 7.0, 8.0, 1234)
	assert.Equal(t, err, entities.ErrInvalidNetworkType)
}

func TestNewLocation_InvalidAreaCode(t *testing.T) {
	// Test with area code too small
	_, err := entities.NewLocation(1, entities.NetworkType2G, "nord", 30.0, 31.0, 7.0, 8.0, 999)
	assert.Equal(t, err, entities.ErrInvalidAreaCode)

	// Test with area code too large
	_, err = entities.NewLocation(1, entities.NetworkType2G, "nord", 30.0, 31.0, 7.0, 8.0, 10000)
	assert.Equal(t, err, entities.ErrInvalidAreaCode)
}
