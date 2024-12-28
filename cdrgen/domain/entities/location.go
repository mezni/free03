package entities

import (
	"errors"
	"fmt"
	"regexp"
	"strings"
)

// Constants for validation boundaries
const (
	MinLatitude  = -90
	MaxLatitude  = 90
	MinLongitude = -180
	MaxLongitude = 180
)

// Custom errors
var (
	ErrInvalidNetworkTechnology = errors.New("invalid network technology")
	ErrInvalidLatitude          = errors.New("latitude must be between -90 and 90 degrees")
	ErrInvalidLongitude         = errors.New("longitude must be between -180 and 180 degrees")
	ErrLatitudeOrder            = errors.New("latMin must be less than or equal to latMax")
	ErrLongitudeOrder           = errors.New("lonMin must be less than or equal to lonMax")
	ErrEmptyLocationName        = errors.New("location name cannot be empty")
	ErrInvalidAreaCode          = errors.New("area code must be a 4-digit number")
)

// Location represents a geographic location.
type Location struct {
	LocationID       int
	NetworkTechnology string
	LocationName     string
	LatMin           float64
	LatMax           float64
	LonMin           float64
	LonMax           float64
	AreaCode         string
}

var validTechnologies = map[string]bool{
	"5G": true, "4G": true, "3G": true, "2G": true,
}

// Validation functions
func IsValidLatitude(lat float64) bool {
	return lat >= MinLatitude && lat <= MaxLatitude
}

func IsValidLongitude(lon float64) bool {
	return lon >= MinLongitude && lon <= MaxLongitude
}

func IsValidAreaCode(areaCode string) bool {
	// Use regex to ensure the string is a 4-digit number
	re := regexp.MustCompile(`^\d{4}$`)
	return re.MatchString(areaCode)
}

func IsValidNetworkTechnology(networkTechnology string) bool {
	_, exists := validTechnologies[strings.ToUpper(networkTechnology)]
	return exists
}

// NewLocation creates a new Location instance.
func NewLocation(
	locationID int,
	networkTechnology, locationName string,
	latMin, latMax, lonMin, lonMax float64,
	areaCode string,
) (*Location, error) {
	if !IsValidNetworkTechnology(networkTechnology) {
		return nil, fmt.Errorf("%w: %s", ErrInvalidNetworkTechnology, networkTechnology)
	}

	if !IsValidLatitude(latMin) || !IsValidLatitude(latMax) {
		return nil, fmt.Errorf("%w: [%f, %f]", ErrInvalidLatitude, latMin, latMax)
	}
	if !IsValidLongitude(lonMin) || !IsValidLongitude(lonMax) {
		return nil, fmt.Errorf("%w: [%f, %f]", ErrInvalidLongitude, lonMin, lonMax)
	}

	if latMin > latMax {
		return nil, ErrLatitudeOrder
	}
	if lonMin > lonMax {
		return nil, ErrLongitudeOrder
	}

	if strings.TrimSpace(locationName) == "" {
		return nil, ErrEmptyLocationName
	}

	if !IsValidAreaCode(areaCode) {
		return nil, fmt.Errorf("%w: %s", ErrInvalidAreaCode, areaCode)
	}

	return &Location{
		LocationID:       locationID,
		NetworkTechnology: networkTechnology,
		LocationName:     locationName,
		LatMin:           latMin,
		LatMax:           latMax,
		LonMin:           lonMin,
		LonMax:           lonMax,
		AreaCode:         areaCode,
	}, nil
}
