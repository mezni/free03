package main

import (
    "fmt"
    "log"
    "os"

    "gopkg.in/yaml.v3"
    "go.etcd.io/bbolt"

    "github.com/mezni/wovoka/cdrgen/application/services"
    "github.com/mezni/wovoka/cdrgen/application/dtos"
)

const (
    dbName            = "locations.db"
    locationBucketName = "Locations" // Changed the bucket name to locationBucketName
    configFile        = "config.yaml"
)

func main() {
    if err := run(); err != nil {
        log.Fatalf("Application error: %v", err)
    }
}

func run() error {
    // Open the BoltDB database
    db, err := bbolt.Open(dbName, 0600, nil)
    if err != nil {
        return fmt.Errorf("failed to open BoltDB: %w", err)
    }
    defer db.Close()

    // Initialize the LocationService with the db instance
    locationService := services.NewLocationService(db)

    // Load configuration from YAML file
    cfgData, err := loadConfig(configFile)
    if err != nil {
        return fmt.Errorf("error loading config: %w", err)
    }

    // Generate locations based on the config data
    locations, err := locationService.GenerateLocations(cfgData)
    if err != nil {
        return fmt.Errorf("error generating locations: %w", err)
    }

    // Save generated locations to BoltDB
    err = locationService.SaveToBoltDB(dbName, locationBucketName, locations)
    if err != nil {
        return fmt.Errorf("error saving to BoltDB: %w", err)
    }

    // Output generated locations to the console
    fmt.Println("Generated Locations:")
    for _, location := range locations {
        fmt.Printf("ID %d, Name '%s' (Tech: %s), Latitude: [%.6f, %.6f], Longitude: [%.6f, %.6f], Area Code: %d\n",
            location.ID, location.Name, location.NetworkTechnology, location.LatitudeMin, location.LatitudeMax, location.LongitudeMin, location.LongitudeMax, location.AreaCode)
    }

    // Read locations from BoltDB and output to the console
    storedLocations, err := locationService.ReadFromBoltDB(locationBucketName)
    if err != nil {
        return fmt.Errorf("error reading from BoltDB: %w", err)
    }

    fmt.Println("\nStored Locations in DB:")
    for _, location := range storedLocations {
        fmt.Printf("ID %d, Name '%s' (Tech: %s), Latitude: [%.6f, %.6f], Longitude: [%.6f, %.6f], Area Code: %d\n",
            location.ID, location.Name, location.NetworkTechnology, location.LatitudeMin, location.LatitudeMax, location.LongitudeMin, location.LongitudeMax, location.AreaCode)
    }

    return nil
}

// loadConfig loads the YAML configuration file and decodes it into CfgData
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
