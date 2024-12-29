package services

import (
	"fmt"
	"math/rand"
	"time"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/application/dtos"
)

// LocationService handles logic for generating locations.
type LocationService struct{}

// Function to generate latitude ranges for each row
func (s *LocationService) generateLatitudeRanges(minLat, maxLat float64, rows int) [][2]float64 {
	step := (maxLat - minLat) / float64(rows)
	latitudeRanges := make([][2]float64, rows)

	for i := 0; i < rows; i++ {
		latitudeRanges[i][0] = minLat + float64(i)*step     // minLatitude for the row
		latitudeRanges[i][1] = minLat + float64(i+1)*step   // maxLatitude for the row
	}

	return latitudeRanges
}

// Function to generate longitude ranges for each column
func (s *LocationService) generateLongitudeRanges(minLong, maxLong float64, cols int) [][2]float64 {
	step := (maxLong - minLong) / float64(cols)
	longitudeRanges := make([][2]float64, cols)

	for i := 0; i < cols; i++ {
		longitudeRanges[i][0] = minLong + float64(i)*step     // minLongitude for the column
		longitudeRanges[i][1] = minLong + float64(i+1)*step   // maxLongitude for the column
	}

	return longitudeRanges
}

// Function to generate AreaCode (5-digit)
func (s *LocationService) generateAreaCode(prefix int) int {
	return prefix*10000 + rand.Intn(10000) // Ensure the AreaCode is always 5 digits
}

// GenerateLocations processes the location splits and generates locations
func (s *LocationService) GenerateLocations(cfgData dtos.CfgData) ([]entities.Location, error) {
	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	var locations []entities.Location
	locationID := 1

	// Process the data
	minLat, maxLat := cfgData.Locations.Latitude[0], cfgData.Locations.Latitude[1]
	minLong, maxLong := cfgData.Locations.Longitude[0], cfgData.Locations.Longitude[1]

	for _, locationSplit := range cfgData.Locations.LocationSplit {
		fmt.Println("Processing NetworkTechnology:", locationSplit.NetworkTechnology)

		latitudeRanges := s.generateLatitudeRanges(minLat, maxLat, locationSplit.SplitRows)
		longitudeRanges := s.generateLongitudeRanges(minLong, maxLong, locationSplit.SplitColumns)

		// Determine AreaCode prefix
		var prefix int
		switch locationSplit.NetworkTechnology {
		case "2G":
			prefix = 2
		case "3G":
			prefix = 3
		case "4G":
			prefix = 4
		default:
			prefix = 0 // Default for unknown technologies
		}

		// Combine rows and columns to generate Location entries
		for i, latRange := range latitudeRanges {
			for j, longRange := range longitudeRanges {
				// Determine the name based on LocationNames and grid position
				var name string
				if i*locationSplit.SplitColumns+j < len(locationSplit.LocationNames) {
					name = locationSplit.LocationNames[i*locationSplit.SplitColumns+j]
				} else {
					name = fmt.Sprintf("Unnamed-%d", locationID)
				}

				// Generate AreaCode
				areaCode := s.generateAreaCode(prefix)

				// Create a Location entry
				location := entities.Location{
					LocationID:        locationID,
					NetworkTechnology: locationSplit.NetworkTechnology,
					Name:              name,
					LatitudeMin:       latRange[0],
					LatitudeMax:       latRange[1],
					LongitudeMin:      longRange[0],
					LongitudeMax:      longRange[1],
					AreaCode:          areaCode,
				}

				// Append to the locations slice
				locations = append(locations, location)

				// Increment LocationID
				locationID++
			}
		}
	}

	return locations, nil
}

