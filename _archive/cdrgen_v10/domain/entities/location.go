package entities

// Location represents a geographic location with its respective network technology and bounding box.
type Location struct {
	LocationID        int
	NetworkTechnology string
	Name              string
	LatitudeMin       float64
	LatitudeMax       float64
	LongitudeMin      float64
	LongitudeMax      float64
	AreaCode          int
}

func IsValidLatitude(latitude float64) bool {
	return latitude >= -90 && latitude <= 90
}

// IsValidLongitude checks if the longitude is within valid bounds.
func IsValidLongitude(longitude float64) bool {
	return longitude >= -180 && longitude <= 180
}

// IsValidAreaCode checks if the AreaCode is valid.
func IsValidAreaCode(areaCode int) bool {
	return areaCode >= 1000 && areaCode <= 9999
}

// NewLocation is a factory function to create a new Location instance.
func NewLocation(
	locationID int,
	networkTechnology string,
	name string,
	latitudeMin, latitudeMax, longitudeMin, longitudeMax float64,
	areaCode int,
) (*Location, error) {
	// Validate network technology
	if networkTechnology == "" { // Check if networkTechnology is empty
		return nil, ErrInvalidNetworkTechnology
	}

	// Validate latitude and longitude bounds
	if !IsValidLatitude(latitudeMin) || !IsValidLatitude(latitudeMax) {
		return nil, ErrInvalidLatitude
	}
	if !IsValidLongitude(longitudeMin) || !IsValidLongitude(longitudeMax) {
		return nil, ErrInvalidLongitude
	}

	// Check if latitudeMin is greater than latitudeMax
	if latitudeMin > latitudeMax {
		return nil, ErrLatitudeOrder
	}

	// Check if longitudeMin is greater than longitudeMax
	if longitudeMin > longitudeMax {
		return nil, ErrLongitudeOrder
	}

	// Validate Name
	if name == "" {
		return nil, ErrEmptyName
	}

	// Validate AreaCode
	if !IsValidAreaCode(areaCode) {
		return nil, ErrInvalidAreaCode
	}

	// Return the new Location instance
	return &Location{
		LocationID:        locationID,
		NetworkTechnology: networkTechnology,
		Name:              name,
		LatitudeMin:       latitudeMin,
		LatitudeMax:       latitudeMax,
		LongitudeMin:      longitudeMin,
		LongitudeMax:      longitudeMax,
		AreaCode:          areaCode,
	}, nil
}
