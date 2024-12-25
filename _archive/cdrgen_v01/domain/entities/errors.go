package entities

import (
	"errors"
)

// Custom errors for validation
var (
	ErrInvalidNetworkType     = errors.New("invalid NetworkType: must be one of 2G, 3G, 4G, 5G")
	ErrEmptyNetworkElementName = errors.New("NetworkElementName cannot be empty")
	ErrInvalidLatitude         = errors.New("invalid latitude: must be between -90 and 90")
	ErrInvalidLongitude        = errors.New("invalid longitude: must be between -180 and 180")
	ErrEmptyLocationName       = errors.New("LocationName cannot be empty")
	ErrLatitudeOrder           = errors.New("latMin cannot be greater than latMax")
	ErrLongitudeOrder          = errors.New("lonMin cannot be greater than lonMax")
	ErrInvalidAreaCode         = errors.New("AreaCode must be a four-digit integer between 1000 and 9999")
)