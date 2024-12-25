package entities

import (
	"errors"
)

// Custom errors for validation
var (
	ErrInvalidNetworkType = errors.New("invalid NetworkType: must be one of 2G, 3G, 4G, 5G")
	ErrInvalidLatitude    = errors.New("invalid latitude: must be between -90 and 90")
	ErrInvalidLongitude   = errors.New("invalid longitude: must be between -180 and 180")
	ErrEmptyLocationName  = errors.New("LocationName cannot be empty")
	ErrLatitudeOrder      = errors.New("latMin cannot be greater than latMax")
	ErrLongitudeOrder     = errors.New("lonMin cannot be greater than lonMax")
	ErrInvalidAreaCode    = errors.New("AreaCode must be a four-digit integer between 1000 and 9999")
)

// NetworkType is a type that represents different network types.
type NetworkType int

// Constants for the available network types.
const (
	NetworkType2G NetworkType = iota
	NetworkType3G
	NetworkType4G
	NetworkType5G
)

// networkTypes is a list of available network types.
var networkTypes = []string{"2G", "3G", "4G", "5G"}

// String returns the string representation of the NetworkType.
func (nt NetworkType) String() string {
	if nt < NetworkType2G || nt > NetworkType5G {
		return "Unknown"
	}
	return networkTypes[nt]
}

// Location struct represents a geographic location.
type Location struct {
	LocationID   int
	NetworkType  NetworkType
	LocationName string
	LatMin       float64
	LatMax       float64
	LonMin       float64
	LonMax       float64
	AreaCode     int
}

// IsValidNetworkType checks if the given NetworkType is valid.
func IsValidNetworkType(networkType NetworkType) bool {
	return networkType >= NetworkType2G && networkType <= NetworkType5G
}

// IsValidLatitude checks if the latitude is within valid bounds.
func IsValidLatitude(lat float64) bool {
	return lat >= -90 && lat <= 90
}

// IsValidLongitude checks if the longitude is within valid bounds.
func IsValidLongitude(lon float64) bool {
	return lon >= -180 && lon <= 180
}

// IsValidAreaCode checks if the AreaCode is valid.
func IsValidAreaCode(areaCode int) bool {
	return areaCode >= 1000 && areaCode <= 9999
}

// NewLocation is a factory function to create a new Location instance.
func NewLocation(
	locationID int,
	networkType NetworkType,
	locationName string,
	latMin, latMax, lonMin, lonMax float64,
	areaCode int,
) (*Location, error) {
	// Validate network type
	if !IsValidNetworkType(networkType) {
		return nil, ErrInvalidNetworkType
	}

	// Validate latitude and longitude bounds
	if !IsValidLatitude(latMin) || !IsValidLatitude(latMax) {
		return nil, ErrInvalidLatitude
	}
	if !IsValidLongitude(lonMin) || !IsValidLongitude(lonMax) {
		return nil, ErrInvalidLongitude
	}

	// Check if latMin is greater than latMax
	if latMin > latMax {
		return nil, ErrLatitudeOrder
	}

	// Check if lonMin is greater than lonMax
	if lonMin > lonMax {
		return nil, ErrLongitudeOrder
	}

	// Validate that LocationName is not empty
	if locationName == "" {
		return nil, ErrEmptyLocationName
	}

	// Validate AreaCode
	if !IsValidAreaCode(areaCode) {
		return nil, ErrInvalidAreaCode
	}

	// Return the new Location instance
	return &Location{
		LocationID:   locationID,
		NetworkType:  networkType,
		LocationName: locationName,
		LatMin:       latMin,
		LatMax:       latMax,
		LonMin:       lonMin,
		LonMax:       lonMax,
		AreaCode:     areaCode,
	}, nil
}
