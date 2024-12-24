package entities

import (
	"testing"
)

func TestNewLocation(t *testing.T) {
	tests := []struct {
		name         string
		locationID   int
		networkType  NetworkType
		locationName string
		latMin       float64
		latMax       float64
		lonMin       float64
		lonMax       float64
		expectedErr  error
	}{
		{
			name:         "valid 2G location",
			locationID:   1,
			networkType:  NetworkType2G,
			locationName: "Downtown",
			latMin:       40.7128,
			latMax:       40.9152,
			lonMin:       -74.0060,
			lonMax:       -73.7004,
			expectedErr:  nil,
		},
		{
			name:         "valid 3G location",
			locationID:   2,
			networkType:  NetworkType3G,
			locationName: "Uptown",
			latMin:       40.7128,
			latMax:       40.9152,
			lonMin:       -74.0060,
			lonMax:       -73.7004,
			expectedErr:  nil,
		},
		{
			name:         "invalid NetworkType",
			locationID:   3,
			networkType:  NetworkType(99), // Invalid NetworkType
			locationName: "Midtown",
			latMin:       40.7128,
			latMax:       40.9152,
			lonMin:       -74.0060,
			lonMax:       -73.7004,
			expectedErr:  ErrInvalidNetworkType,
		},
		{
			name:         "empty LocationName",
			locationID:   4,
			networkType:  NetworkType4G,
			locationName: "",
			latMin:       40.7128,
			latMax:       40.9152,
			lonMin:       -74.0060,
			lonMax:       -73.7004,
			expectedErr:  ErrEmptyLocationName,
		},
		{
			name:         "invalid latitude",
			locationID:   5,
			networkType:  NetworkType5G,
			locationName: "Suburb",
			latMin:       -100, // Invalid latitude
			latMax:       40.9152,
			lonMin:       -74.0060,
			lonMax:       -73.7004,
			expectedErr:  ErrInvalidLatitude,
		},
		{
			name:         "invalid longitude",
			locationID:   6,
			networkType:  NetworkType4G,
			locationName: "Beach",
			latMin:       40.7128,
			latMax:       40.9152,
			lonMin:       -190, // Invalid longitude
			lonMax:       -73.7004,
			expectedErr:  ErrInvalidLongitude,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			location, err := NewLocation(tt.locationID, tt.networkType, tt.locationName, tt.latMin, tt.latMax, tt.lonMin, tt.lonMax)

			if err != nil && err != tt.expectedErr {
				t.Errorf("expected error %v, got %v", tt.expectedErr, err)
			}
			if err == nil && tt.expectedErr != nil {
				t.Errorf("expected error %v, but got none", tt.expectedErr)
			}

			if err == nil {
				// Check if the returned location is correct
				if location.LocationID != tt.locationID {
					t.Errorf("expected LocationID %d, got %d", tt.locationID, location.LocationID)
				}
				if location.NetworkType != tt.networkType {
					t.Errorf("expected NetworkType %v, got %v", tt.networkType, location.NetworkType)
				}
				if location.LocationName != tt.locationName {
					t.Errorf("expected LocationName %s, got %s", tt.locationName, location.LocationName)
				}
			}
		})
	}
}
