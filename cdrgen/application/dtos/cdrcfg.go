package dtos

type LocationSplit struct {
    NetworkTechnology string   `yaml:"NetworkTechnology"`
    SplitRows         int      `yaml:"SplitRows"`
    SplitColumns      int      `yaml:"SplitColumns"`
    LocationNames     []string `yaml:"LocationNames"`
}

type LocationsConfig struct {
    Latitude      []float64      `yaml:"Latitude"`
    Longitude     []float64      `yaml:"Longitude"`
    LocationSplit []LocationSplit `yaml:"LocationSplit"`
}

type CfgData struct {
    Locations LocationsConfig `yaml:"Locations"`
}