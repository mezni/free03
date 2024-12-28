package services

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
)

// BaselineLoaderService handles loading and processing baseline data
type BaselineLoaderService struct{}

// LoadData reads and processes baseline data from a JSON file
func (b *BaselineLoaderService) LoadData(filename string) (map[string]interface{}, error) {
	// Open the JSON file
	file, err := os.Open(filename)
	if err != nil {
		return nil, fmt.Errorf("error opening file: %v", err)
	}
	defer file.Close()

	// Read the file into a byte slice
	byteValue, err := ioutil.ReadAll(file)
	if err != nil {
		return nil, fmt.Errorf("error reading file: %v", err)
	}

	// Declare a variable to hold the unmarshaled JSON
	var data dtos.ConfigData

	// Unmarshal the JSON data into the struct
	if err = json.Unmarshal(byteValue, &data); err != nil {
		return nil, fmt.Errorf("error unmarshaling data: %v", err)
	}

	// Create a BaselineMapper instance
	mapper := &mappers.BaselineMapper{}

	// Map DTOs to domain entities
	networkTechnologies, err := mapper.ToNetworkTechnologies(data.NetworkTechnologies)
	if err != nil {
		return nil, fmt.Errorf("error mapping network technologies: %v", err)
	}

	networkElementTypes, err := mapper.ToNetworkElementTypes(data.NetworkElementTypes)
	if err != nil {
		return nil, fmt.Errorf("error mapping network element types: %v", err)
	}

	serviceTypes, err := mapper.ToServiceTypes(data.ServiceTypes)
	if err != nil {
		return nil, fmt.Errorf("error mapping service types: %v", err)
	}

	// Aggregate results in a map for easier consumption
	result := map[string]interface{}{
		"NetworkTechnologies": networkTechnologies,
		"NetworkElementTypes": networkElementTypes,
		"ServiceTypes":        serviceTypes,
	}

	return result, nil
}
