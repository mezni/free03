package config

import (
    "fmt"
    "os"
    "gopkg.in/yaml.v3"
    "github.com/mezni/wovoka/cdrgen/application/dtos"
)

// LoadConfig loads the YAML configuration file into a CfgData struct
func LoadConfig(filename string) (dtos.CfgData, error) {
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