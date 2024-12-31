package mappers

import (
	"encoding/json"
	"errors"
	"strconv"
)

// mapToStruct helps to decode a map[string]interface{} into a target struct
func MapToStruct(data map[string]interface{}, result interface{}) error {
	// Marshal the map into JSON (which is []byte), then unmarshal into the target struct
	byteData, err := json.Marshal(data)
	if err != nil {
		return errors.New("failed to marshal map to byte data")
	}
	return json.Unmarshal(byteData, result)
}

// ConvertSliceToMaps converts a slice of any type into a slice of maps, adding sequential IDs
func ConvertSliceToMaps[T any](slice []T) ([]map[string]interface{}, error) {
	var result []map[string]interface{}

	for i, item := range slice {
		// Convert each item to JSON
		itemJSON, err := json.Marshal(item)
		if err != nil {
			return nil, errors.New("error marshalling item")
		}

		// Convert JSON to map
		itemMap := make(map[string]interface{})
		err = json.Unmarshal(itemJSON, &itemMap)
		if err != nil {
			return nil, errors.New("error unmarshalling item JSON")
		}

		// Add the sequential ID (starting from 1)
		itemMap["ID"] = strconv.Itoa(i + 1)

		// Append the map to the result slice
		result = append(result, itemMap)
	}

	return result, nil
}
