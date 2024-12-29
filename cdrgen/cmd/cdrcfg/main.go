package main

import (
    "fmt"
    "log"
    "os"

    "gopkg.in/yaml.v3"
    "github.com/mezni/wovoka/cdrgen/application/services"
    "github.com/mezni/wovoka/cdrgen/application/dtos"
)

const (
    dbName     = "locations.db"
    bucketName = "Locations"
    configFile = "config.yaml"
)

func main() {
    if err := run(); err != nil {
        log.Fatalf("Application error: %v", err)
    }
}

func run() error {
    // Initialize the LocationService
    locationService := &services.LocationService{}

    // Load configuration from YAML file
    cfgData, err := loadConfig(configFile)
    if err != nil {
        return fmt.Errorf("error loading config: %w", err)
    }

    // Generate locations
    locations, err := locationService.GenerateLocations(cfgData)
    if err != nil {
        return fmt.Errorf("error generating locations: %w", err)
    }

    // Save generated locations to BoltDB
    err = locationService.SaveToBoltDB(dbName, bucketName, locations)
    if err != nil {
        return fmt.Errorf("error saving to BoltDB: %w", err)
    }

    // Output generated locations
    for _, location := range locations {
        fmt.Printf("Generated Location: ID %d, Name '%s' (Tech: %s), Latitude: [%.6f, %.6f], Longitude: [%.6f, %.6f], Area Code: %d\n",
            location.ID, location.Name, location.NetworkTechnology, location.LatitudeMin, location.LatitudeMax, location.LongitudeMin, location.LongitudeMax, location.AreaCode)
    }

    // Read locations from BoltDB
    storedLocations, err := locationService.ReadFromBoltDB(dbName, bucketName)
    if err != nil {
        return fmt.Errorf("error reading from BoltDB: %w", err)
    }

    // Output stored locations
    for _, location := range storedLocations {
        fmt.Printf("Stored Location: ID %d, Name '%s' (Tech: %s), Latitude: [%.6f, %.6f], Longitude: [%.6f, %.6f], Area Code: %d\n",
            location.ID, location.Name, location.NetworkTechnology, location.LatitudeMin, location.LatitudeMax, location.LongitudeMin, location.LongitudeMax, location.AreaCode)
    }

    return nil
}

func loadConfig(filename string) (dtos.CfgData, error) {
    file, err := os.Open(filename)
    if err != nil {
        return dtos.CfgData{}, fmt.Errorf("error opening config file: %w", err)
    }
    defer file.Close()

    var cfg dtos.CfgData
    decoder := yaml.NewDecoder(file)
    if err := decoder.Decode(&cfg); err != nil {
        return dtos.CfgData{}, fmt.Errorf("error decoding config file: %w", err)
    }

    return cfg, nil
}