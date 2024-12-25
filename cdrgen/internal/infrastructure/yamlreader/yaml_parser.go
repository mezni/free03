package yamlreader

import (
	"gopkg.in/yaml.v3"
	"io/ioutil"
	"os"
)

// ReadYAML reads a YAML file and unmarshals its contents into the provided target.
// The target can be either a struct or a map[string]interface{} for generic usage.
func ReadYAML(filePath string, target interface{}) error {
	file, err := os.Open(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	content, err := ioutil.ReadAll(file)
	if err != nil {
		return err
	}

	if err := yaml.Unmarshal(content, target); err != nil {
		return err
	}

	return nil
}
