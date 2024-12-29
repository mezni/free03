package services

import (
    "fmt"

)

type LocationService struct {

    
}

func NewLocationService() (*LocationService, error) {
    return &LocationService{
    }, nil
}    

func (s *LocationService) LoadToDB(configData map[string]interface{}) error {
	if configData == nil {
		return fmt.Errorf("config file data is empty")
	}

	// Step 2: Extract specific values from the config map
	country := configData["Country"].(string)
	coordinates := configData["Coordinates"].(map[string]interface{})
	latitude := coordinates["Latitude"].([]interface{})
	longitude := coordinates["Longitude"].([]interface{})

	// Step 3: Parse Networks data
	networks := configData["Networks"].(map[string]interface{})


	for networkType, networkDetails := range networks {
		fmt.Println(networkType, networkDetails)
	}

	// Example: Print out the extracted data
	fmt.Println("Country:", country)
	fmt.Println("Coordinates - Latitude:", latitude)
	fmt.Println("Coordinates - Longitude:", longitude)

    return nil
}
