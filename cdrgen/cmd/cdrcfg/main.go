package main

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v3"
	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/application/services"
)

func main() {
	// Specify the file path
	filePath := "config.yaml"

	// Read the YAML file
	yamlData, err := os.ReadFile(filePath)
	if err != nil {
		fmt.Printf("Error reading file '%s': %v\n", filePath, err)
		return
	}

	// Unmarshal the YAML data into a CfgData struct
	var cfgData dtos.CfgData
	err = yaml.Unmarshal(yamlData, &cfgData)
	if err != nil {
		fmt.Printf("Error unmarshaling YAML: %v\n", err)
		return
	}

	// Initialize LocationService
	locationService := services.LocationService{}

	// Generate locations using the service
	locations, err := locationService.GenerateLocations(cfgData)
	if err != nil {
		fmt.Printf("Error generating locations: %v\n", err)
		return
	}

	// Print all locations
	for _, location := range locations {
		fmt.Printf("LocationID: %d, Name: %s, Network: %s, Lat: [%.2f, %.2f], Long: [%.2f, %.2f], AreaCode: %05d\n",
			location.LocationID, location.Name, location.NetworkTechnology,
			location.LatitudeMin, location.LatitudeMax,
			location.LongitudeMin, location.LongitudeMax, location.AreaCode)
	}
}
