package factories

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"math/rand"
	"time"
)

// GenerateLocations generates locations based on the provided configuration.
func GenerateLocations(config *mappers.Config) ([]*entities.Location, error) {
	var locations []*entities.Location
	locationID := 1

	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	for networkType, networkData := range config.Networks {
		latRange := config.Coordinates.Latitude[1] - config.Coordinates.Latitude[0]
		lonRange := config.Coordinates.Longitude[1] - config.Coordinates.Longitude[0]
		latStep := latRange / float64(networkData.Rows)
		lonStep := lonRange / float64(networkData.Columns)

		if len(networkData.LocationNames) != networkData.Rows*networkData.Columns {
			return nil, fmt.Errorf("mismatch between location names and grid dimensions for network %s", networkType)
		}

		// Generate grid locations for the network
		index := 0
		for row := 0; row < networkData.Rows; row++ {
			for col := 0; col < networkData.Columns; col++ {
				latMin := config.Coordinates.Latitude[0] + latStep*float64(row)
				latMax := latMin + latStep
				lonMin := config.Coordinates.Longitude[0] + lonStep*float64(col)
				lonMax := lonMin + lonStep

				locationName := networkData.LocationNames[index]
				index++

				// Generate area code based on network type
				var areaCode string
				switch networkType {
				case "2G":
					areaCode = fmt.Sprintf("2%03d", rand.Intn(1000)) // Concatenate "2" with 3 random digits
				case "3G":
					areaCode = fmt.Sprintf("3%03d", rand.Intn(1000)) // Concatenate "3" with 3 random digits
				case "4G":
					areaCode = fmt.Sprintf("4%03d", rand.Intn(1000)) // Concatenate "4" with 3 random digits
				default:
					areaCode = fmt.Sprintf("%d%03d", locationID, rand.Intn(1000)) // For other network types, use default
				}

				// Create the location entity with the locationID and dynamically generated AreaCode
				location := &entities.Location{
					ID:                locationID,
					NetworkTechnology: networkType,
					Name:              locationName,
					LatitudeMin:       latMin,
					LatitudeMax:       latMax,
					LongitudeMin:      lonMin,
					LongitudeMax:      lonMax,
					AreaCode:          areaCode, // Using the generated area code
				}

				locations = append(locations, location)
				locationID++
			}
		}
	}

	return locations, nil
}
