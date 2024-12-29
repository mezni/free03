package mappers

import (
	"fmt"
	"math/rand"
	"time"

	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// LocationMapper handles logic for generating and managing locations.
type LocationMapper struct{}

// NewLocationMapper initializes a LocationMapper.
func NewLocationMapper() *LocationMapper {
	return &LocationMapper{}
}

// GenerateLatitudeRanges generates latitude ranges for each row.
func (m *LocationMapper) GenerateLatitudeRanges(minLat, maxLat float64, rows int) [][2]float64 {
	step := (maxLat - minLat) / float64(rows)
	latitudeRanges := make([][2]float64, rows)

	for i := 0; i < rows; i++ {
		latitudeRanges[i][0] = minLat + float64(i)*step     // minLatitude for the row
		latitudeRanges[i][1] = minLat + float64(i+1)*step   // maxLatitude for the row
	}

	return latitudeRanges
}

// GenerateLongitudeRanges generates longitude ranges for each column.
func (m *LocationMapper) GenerateLongitudeRanges(minLong, maxLong float64, cols int) [][2]float64 {
	step := (maxLong - minLong) / float64(cols)
	longitudeRanges := make([][2]float64, cols)

	for i := 0; i < cols; i++ {
		longitudeRanges[i][0] = minLong + float64(i)*step     // minLongitude for the column
		longitudeRanges[i][1] = minLong + float64(i+1)*step   // maxLongitude for the column
	}

	return longitudeRanges
}

// GenerateAreaCode generates a 5-digit area code based on the network technology prefix.
func (m *LocationMapper) GenerateAreaCode(prefix int) int {
	return prefix*10000 + rand.Intn(10000) // Ensure the AreaCode is always 5 digits
}

// GetNetworkTechnologyPrefix returns the prefix based on the network technology.
func (m *LocationMapper) GetNetworkTechnologyPrefix(networkTechnology string) int {
	switch networkTechnology {
	case "2G":
		return 2
	case "3G":
		return 3
	case "4G":
		return 4
	case "5G":
		return 5
	default:
		return 0 // Default for unknown technologies
	}
}

// LocationService handles application-level logic for processing locations.
type LocationService struct {
	mapper *LocationMapper
}

// NewLocationService initializes a LocationService.
func NewLocationService() *LocationService {
	return &LocationService{mapper: NewLocationMapper()}
}

// IsValidNetworkTechnology checks if the given network technology is valid.
func (s *LocationService) IsValidNetworkTechnology(networkTechnology string) bool {
	validNetworkTechnologies := []string{"2G", "3G", "4G", "5G"}
	for _, validTech := range validNetworkTechnologies {
		if networkTechnology == validTech {
			return true
		}
	}
	return false
}

// GenerateLocations processes the entire CfgData struct and generates locations.
func (s *LocationService) GenerateLocations(cfgData dtos.CfgData) ([]entities.Location, error) {
	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	var locations []entities.Location
	locationID := 1

	// Extract min/max latitudes and longitudes
	minLat, maxLat := cfgData.Locations.Latitude[0], cfgData.Locations.Latitude[1]
	minLong, maxLong := cfgData.Locations.Longitude[0], cfgData.Locations.Longitude[1]

	// Iterate through the LocationSplits
	for _, locationSplit := range cfgData.Locations.LocationSplit {
		// Validate NetworkTechnology
		if !s.IsValidNetworkTechnology(locationSplit.NetworkTechnology) {
			return nil, fmt.Errorf("invalid NetworkTechnology: %s, must be one of: %v", locationSplit.NetworkTechnology, []string{"2G", "3G", "4G", "5G"})
		}


		latitudeRanges := s.mapper.GenerateLatitudeRanges(minLat, maxLat, locationSplit.SplitRows)
		longitudeRanges := s.mapper.GenerateLongitudeRanges(minLong, maxLong, locationSplit.SplitColumns)

		// Get the prefix based on the network technology
		prefix := s.mapper.GetNetworkTechnologyPrefix(locationSplit.NetworkTechnology)

		// Combine rows and columns to generate Location entries
		for i, latRange := range latitudeRanges {
			for j, longRange := range longitudeRanges {
				var name string
				if i*locationSplit.SplitColumns+j < len(locationSplit.LocationNames) {
					name = locationSplit.LocationNames[i*locationSplit.SplitColumns+j]
				} else {
					name = fmt.Sprintf("Unnamed-%d", locationID)
				}

				// Generate AreaCode
				areaCode := s.mapper.GenerateAreaCode(prefix)

				// Use NewLocation to create a Location entry
				location, err := entities.NewLocation(locationID, locationSplit.NetworkTechnology, name, latRange[0], latRange[1], longRange[0], longRange[1], areaCode)
				if err != nil {
					return nil, fmt.Errorf("failed to create location: %v", err)
				}

				locations = append(locations, *location)
				locationID++
			}
		}
	}

	return locations, nil
}
