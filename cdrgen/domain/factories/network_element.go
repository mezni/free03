package factories

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"math/rand"
	"time"
)

// GenerateNetworkElements generates a list of NetworkElements based on NetworkElementTypes and Locations.
func GenerateNetworkElements(networkElementTypes []*entities.NetworkElementType, locations []*entities.Location) ([]*entities.NetworkElement, error) {
	if len(networkElementTypes) == 0 || len(locations) == 0 {
		return nil, fmt.Errorf("no network element types or locations provided")
	}

	var networkElements []*entities.NetworkElement
	rand.Seed(time.Now().UnixNano())

	// Map of special element types requiring 20 elements per location
	specialElementTypes := map[string]bool{
		"BSC":     true,
		"NodeBs":  true,
		"eNodeBs": true,
		"gNodeB":  true,
	}

	for _, netElemType := range networkElementTypes {
		for _, loc := range locations {
			// Match locations with the same NetworkTechnology
			if loc.NetworkTechnology != netElemType.NetworkTechnology {
				continue
			}

			// Determine number of elements to generate
			var elementCount int
			if specialElementTypes[netElemType.Name] {
				elementCount = 20
			} else {
				elementCount = 1 // Only one element per technology if it's not in specialElementTypes
			}

			for i := 0; i < elementCount; i++ {
				networkElement := &entities.NetworkElement{
					Name:              fmt.Sprintf("%s-%s-%s-%d", netElemType.NetworkTechnology, netElemType.Name, loc.Name, rand.Intn(1000)),
					Description:       fmt.Sprintf("Network element of type %s located at %s", netElemType.Name, loc.Name),
					NetworkTechnology: netElemType.NetworkTechnology,
					IPAddress:         fmt.Sprintf("192.168.%d.%d", rand.Intn(256), rand.Intn(256)), // Random IP address
					Status:            "active",                                                  // Default status
				}

				// Assign LAC or TAC based on NetworkTechnology
				if netElemType.NetworkTechnology == "2G" || netElemType.NetworkTechnology == "3G" {
					networkElement.LAC = &loc.AreaCode
				} else {
					networkElement.TAC = &loc.AreaCode
				}

				// Generate CellID only for specialElementTypes
				cellID := fmt.Sprintf("%04d", rand.Intn(10000))
				if specialElementTypes[netElemType.Name] {
					networkElement.CellID = &cellID
				}

				// Add the generated element to the list
				networkElements = append(networkElements, networkElement)
			}
		}
	}

	return networkElements, nil
}
