package main

import (
	"fmt"
	"os"

	"github.com/mezni/wovoka/cdrgen/infrastructure/filestore"
	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
)

// Define a custom error
var ErrFailedToDecodeJSON = fmt.Errorf("failed to decode JSON")

func main() {
	// Read JSON file into bytes or string
	data, err := filestore.ReadJSONFromFile("baseline.json")
	if err != nil {
		fmt.Println("Error reading JSON file:", err)
		os.Exit(1) // Exit program if the file cannot be read
	}

	// Decode the map into BaselineConfig struct
	var baselineConfig dtos.BaselineConfig
	// If `data` is already a map, you should directly decode it to the target struct
	if err := mappers.MapToStruct(data, &baselineConfig); err != nil {
		fmt.Println("Error decoding JSON into struct:", err)
		os.Exit(1)
	}
	fmt.Println(baselineConfig)
}
