package main

import (
	"fmt"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
)

func main() {
	// Step 2: Prepare data to save (NetworkTechnology instances)
	networkTechnologies := []entities.NetworkTechnology{
		{ID: 1, Name: "5G", Description: "Fifth Generation Mobile Network"},
		{ID: 2, Name: "Wi-Fi 6", Description: "Latest Wi-Fi standard"},
		{ID: 3, Name: "LTE", Description: "4G mobile network technology"},
	}

	// Initialize the NetworkTechnologyMapper
	mapper := mappers.NewMapper[entities.NetworkTechnology]()

	// Convert the slice of entities to a slice of maps
	mapped, err := mapper.ToListMap(networkTechnologies)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Print the mapped data
	fmt.Println("Mapped Data:", mapped)
}
