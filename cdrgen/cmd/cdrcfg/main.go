package main

import (
    "fmt"
    "os"
    "gopkg.in/yaml.v3"
)

// LocationData represents the locations data
type LocationData struct {
    Locations struct {
        Latitude      []float64 `yaml:"Latitude"`
        Longitude     []float64 `yaml:"Longitude"`
        LocationSplit []struct {
            NetworkTechnology string   `yaml:"NetworkTechnology"`
            SplitRows          int      `yaml:"SplitRows"`
            SplitColumns       int      `yaml:"SplitColumns"`
            LocationNames      []string `yaml:"LocationNames"`
        } `yaml:"LocationSplit"`
    } `yaml:"Locations"`
}

func main() {
    // Specify the file path
    filePath := "config.yaml"

    // Read the YAML file
    yamlData, err := os.ReadFile(filePath)
    if err != nil {
        fmt.Printf("Error reading file '%s': %v\n", filePath, err)
        return
    }

    // Unmarshal the YAML data into a LocationData struct
    var locationData LocationData
    err = yaml.Unmarshal(yamlData, &locationData)
    if err != nil {
        fmt.Printf("Error unmarshaling YAML: %v\n", err)
        return
    }

    // Access and print the data
    fmt.Println("Latitude:", locationData.Locations.Latitude)
    fmt.Println("Longitude:", locationData.Locations.Longitude)
    for _, locationSplit := range locationData.Locations.LocationSplit {
        fmt.Println("NetworkTechnology:", locationSplit.NetworkTechnology, locationSplit.SplitRows, locationSplit.SplitColumns, locationSplit.LocationNames)
    }
}
