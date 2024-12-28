package main

import (
	"fmt"


	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/application/services"
)

func main() {
	service := &services.BaselineLoaderService{}

	// Load baseline data
	result, err := service.LoadData("baseline.json")
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	// Access individual entity lists
	networkTechnologies := result["NetworkTechnologies"].([]entities.NetworkTechnology)
	networkElementTypes := result["NetworkElementTypes"].([]entities.NetworkElementType)
	serviceTypes := result["ServiceTypes"].([]entities.ServiceType)

	fmt.Println("Network Technologies:", networkTechnologies)
	fmt.Println("Network Element Types:", networkElementTypes)
	fmt.Println("Service Types:", serviceTypes)

	fmt.Println("XXX:", result["NetworkTechnologies"])
}
