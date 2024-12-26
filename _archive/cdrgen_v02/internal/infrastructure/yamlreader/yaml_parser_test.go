package yamlreader_test

import (
	"os"
	"testing"

	"github.com/mezni/wovoka/cdrgen/internal/infrastructure/yamlreader"
)

// TestReadYAMLWithStruct tests reading a YAML file into a predefined struct.
func TestReadYAMLWithStruct(t *testing.T) {
	// Create a temporary YAML file for testing
	yamlContent := `
app:
  name: "Test App"
  version: "0.1.0"
database:
  host: "localhost"
  port: 5432
  username: "user"
  password: "pass"
`
	tempFile, err := os.CreateTemp("", "config-*.yaml")
	if err != nil {
		t.Fatalf("Failed to create temp file: %v", err)
	}
	defer os.Remove(tempFile.Name()) // Cleanup after the test

	if _, err := tempFile.Write([]byte(yamlContent)); err != nil {
		t.Fatalf("Failed to write to temp file: %v", err)
	}
	tempFile.Close()

	// Define the struct to unmarshal into
	type Config struct {
		App struct {
			Name    string `yaml:"name"`
			Version string `yaml:"version"`
		} `yaml:"app"`
		Database struct {
			Host     string `yaml:"host"`
			Port     int    `yaml:"port"`
			Username string `yaml:"username"`
			Password string `yaml:"password"`
		} `yaml:"database"`
	}

	var config Config
	if err := yamlreader.ReadYAML(tempFile.Name(), &config); err != nil { // Use yamlreader.ReadYAML
		t.Fatalf("Failed to read YAML: %v", err)
	}

	// Validate the contents
	if config.App.Name != "Test App" {
		t.Errorf("Expected App.Name to be 'Test App', got '%s'", config.App.Name)
	}
	if config.App.Version != "0.1.0" {
		t.Errorf("Expected App.Version to be '0.1.0', got '%s'", config.App.Version)
	}
	if config.Database.Host != "localhost" {
		t.Errorf("Expected Database.Host to be 'localhost', got '%s'", config.Database.Host)
	}
	if config.Database.Port != 5432 {
		t.Errorf("Expected Database.Port to be 5432, got '%d'", config.Database.Port)
	}
}

// TestReadYAMLWithMap tests reading a YAML file into a generic map.
func TestReadYAMLWithMap(t *testing.T) {
	// Create a temporary YAML file for testing
	yamlContent := `
locations:
  - id: 1
    name: "New York"
  - id: 2
    name: "London"
services:
  - id: 1
    name: "VoIP"
  - id: 2
    name: "Internet"
`
	tempFile, err := os.CreateTemp("", "data-*.yaml")
	if err != nil {
		t.Fatalf("Failed to create temp file: %v", err)
	}
	defer os.Remove(tempFile.Name()) // Cleanup after the test

	if _, err := tempFile.Write([]byte(yamlContent)); err != nil {
		t.Fatalf("Failed to write to temp file: %v", err)
	}
	tempFile.Close()

	// Define a generic map
	var data map[string]interface{}
	if err := yamlreader.ReadYAML(tempFile.Name(), &data); err != nil { // Use yamlreader.ReadYAML
		t.Fatalf("Failed to read YAML: %v", err)
	}

	// Validate the contents
	locations, ok := data["locations"].([]interface{})
	if !ok {
		t.Fatalf("Expected 'locations' to be a slice, got %T", data["locations"])
	}

	if len(locations) != 2 {
		t.Errorf("Expected 2 locations, got %d", len(locations))
	}

	firstLocation := locations[0].(map[string]interface{})
	if firstLocation["name"] != "New York" {
		t.Errorf("Expected first location name to be 'New York', got '%s'", firstLocation["name"])
	}
}
