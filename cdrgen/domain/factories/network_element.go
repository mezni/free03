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
		"BSC":    true,
		"NodeB":  true,
		"eNodeB": true,
		"gNodeB": true,
	}

	// Iterate over the network element types
	for _, netElemType := range networkElementTypes {
		// Determine the number of elements to generate for each network element type
		var elementCount int
		if specialElementTypes[netElemType.Name] {
			elementCount = 20 // Special element types generate 20 elements per location
		} else {
			elementCount = 1 // Only one element per technology for non-special types
		}

		// If it's not in specialElementTypes, don't enter the location loop
		if !specialElementTypes[netElemType.Name] {
			// Create a single element without considering locations
			networkElement := &entities.NetworkElement{
				Name:              fmt.Sprintf("%s-%s-%d", netElemType.NetworkTechnology, netElemType.Name, rand.Intn(10000)),
				Description:       fmt.Sprintf("Network element of type %s", netElemType.Name),
				ElementType:       netElemType.Name,
				NetworkTechnology: netElemType.NetworkTechnology,
				IPAddress:         fmt.Sprintf("192.168.%d.%d", rand.Intn(256), rand.Intn(256)), // Random IP address
				Status:            "active",                                                     // Default status
			}

			// Assign LAC or TAC based on NetworkTechnology (leave nil for non-special elements)
			if netElemType.NetworkTechnology == "2G" || netElemType.NetworkTechnology == "3G" {
				networkElement.LAC = nil // No location-specific data for non-special elements
			} else {
				networkElement.TAC = nil // No location-specific data for non-special elements
			}
			networkElement.CellID = nil // CellID is not applicable for non-special types

			// Add the generated element to the list
			networkElements = append(networkElements, networkElement)
		} else {
			// If it's in specialElementTypes, create elements for each location
			for _, loc := range locations {
				// Match locations with the same NetworkTechnology
				if loc.NetworkTechnology == netElemType.NetworkTechnology {
					for i := 0; i < elementCount; i++ {

						networkElement := &entities.NetworkElement{
							Name:              fmt.Sprintf("%s-%s-%s-%d", netElemType.NetworkTechnology, netElemType.Name, loc.Name, rand.Intn(10000)),
							Description:       fmt.Sprintf("Network element of type %s located at %s", netElemType.Name, loc.Name),
							ElementType:       netElemType.Name,
							NetworkTechnology: netElemType.NetworkTechnology,
							IPAddress:         fmt.Sprintf("192.168.%d.%d", rand.Intn(256), rand.Intn(256)), // Random IP address
							Status:            "active",                                                     // Default status
						}

						// Assign LAC or TAC based on NetworkTechnology
						if netElemType.NetworkTechnology == "2G" || netElemType.NetworkTechnology == "3G" {
							networkElement.LAC = &loc.AreaCode
						} else {
							networkElement.TAC = &loc.AreaCode
						}

						// Generate CellID only for specialElementTypes
						if specialElementTypes[netElemType.Name] {
							cellID := fmt.Sprintf("%04d", rand.Intn(10000))
							networkElement.CellID = &cellID
						}
						// Add the generated element to the list
						networkElements = append(networkElements, networkElement)
					}
				}
			}
		}
	}

	return networkElements, nil
}
