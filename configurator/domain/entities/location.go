package entities

import "errors"

// NetworkType represents the type of network.
type NetworkType int

// Network type constants
const (
	NetworkType2G NetworkType = iota
	NetworkType3G
	NetworkType4G
	NetworkType5G
)

// Location represents a geographical location.
type Location struct {
	LocationID   int
	NetworkType  NetworkType
	LocationName string
	LatMin       float64
	LatMax       float64
	LonMin       float64
	LonMax       float64
}

// NewLocation creates a new Location instance with validation.
func NewLocation(locationID int, networkType NetworkType, locationName string, latMin, latMax, lonMin, lonMax float64) (*Location, error) {
	if locationName == "" {
		return nil, ErrEmptyLocationName
	}
	if latMin < -90 || latMin > 90 || latMax < -90 || latMax > 90 {
		return nil, ErrInvalidLatitude
	}
	if lonMin < -180 || lonMin > 180 || lonMax < -180 || lonMax > 180 {
		return nil, ErrInvalidLongitude
	}
	if networkType < NetworkType2G || networkType > NetworkType5G {
		return nil, ErrInvalidNetworkType
	}

	return &Location{
		LocationID:   locationID,
		NetworkType:  networkType,
		LocationName: locationName,
		LatMin:       latMin,
		LatMax:       latMax,
		LonMin:       lonMin,
		LonMax:       lonMax,
	}, nil
}

// Custom error messages
var (
	ErrEmptyLocationName  = errors.New("location name cannot be empty")
	ErrInvalidLatitude    = errors.New("invalid latitude value")
	ErrInvalidLongitude   = errors.New("invalid longitude value")
	ErrInvalidNetworkType = errors.New("invalid network type")
)
