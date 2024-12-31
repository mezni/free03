package filestore

import (
	"encoding/json"
	"errors"
	"os"
)

// Define custom error variables
var (
	ErrFailedToOpenFile   = errors.New("failed to open JSON file")
	ErrFailedToDecodeJSON = errors.New("failed to decode JSON")
	ErrFileDoesNotExist   = errors.New("file does not exist")
)

// ReadJSONFromFile reads JSON from a file and parses it into map[string]interface{}
func ReadJSONFromFile(filename string) (map[string]interface{}, error) {
	// Open the file
	file, err := os.Open(filename)
	if err != nil {
		if os.IsNotExist(err) {
			// Return custom error directly for file not found
			return nil, ErrFileDoesNotExist
		}
		// Return custom error for failed file opening
		return nil, ErrFailedToOpenFile
	}
	defer file.Close()

	// Variable to store the parsed JSON
	var result map[string]interface{}

	// Decode the JSON from the file
	decoder := json.NewDecoder(file)
	err = decoder.Decode(&result)
	if err != nil {
		// Return custom error for decoding failure
		return nil, ErrFailedToDecodeJSON
	}

	return result, nil
}
