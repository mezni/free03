package yamlreader

import (
	"io/ioutil"

	"gopkg.in/yaml.v3"
)

type ConfigReader struct {
	filePath string
}

func NewConfigReader(filePath string) *ConfigReader {
	return &ConfigReader{filePath: filePath}
}

// Read reads the YAML file and returns the contents as a map[string]interface{}
func (r *ConfigReader) Read() (map[string]interface{}, error) {
	data, err := ioutil.ReadFile(r.filePath)
	if err != nil {
		return nil, err
	}

	var config map[string]interface{}
	if err := yaml.Unmarshal(data, &config); err != nil {
		return nil, err
	}

	return config, nil
}
