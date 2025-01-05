package interfaces

import (
	"fmt"
	"io/ioutil"

	"gopkg.in/yaml.v3"

	"github.com/mezni/wovoka/cdrgen/application/mappers"
)

// ReadBusinessConfig reads and parses a YAML configuration file into a BusinessConfig struct.
func ReadBusinessConfig(yamlFilename string) (*mappers.BusinessConfig, error) {
	// Read the YAML file
	data, err := ioutil.ReadFile(yamlFilename)
	if err != nil {
		return nil, fmt.Errorf("could not read YAML file: %v", err)
	}

	// Unmarshal YAML data into the BusinessConfig struct
	var config mappers.BusinessConfig
	if err := yaml.Unmarshal(data, &config); err != nil {
		return nil, fmt.Errorf("could not unmarshal YAML: %v", err)
	}

	return &config, nil
}
