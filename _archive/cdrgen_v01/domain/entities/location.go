package entities


// Location represents a geographic location with its respective network type and bounding box.
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

	// Validate LocationName
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
