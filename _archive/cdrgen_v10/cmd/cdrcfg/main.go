package main

import (
//	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/infrastructure/yamlreader" 
	"github.com/mezni/wovoka/cdrgen/application/services" 
)

func main() {
	// Initialize the ConfigReader
	configReader := yamlreader.NewConfigReader("config.yaml")

	// Read the configuration
	configData, err := configReader.Read()
	if err != nil {
		log.Fatalf("Error reading config: %v", err)
	}

	locationService, err := services.NewLocationService()
	if err != nil {
		log.Fatalf("Error creating location service: %v", err)
	}
	_=locationService.LoadToDB(configData)
}
