package mappers

import (
	"encoding/json"
	"fmt"
)

// ConvertSliceToMaps converts a slice of structs to a slice of maps with sequential IDs.
func ConvertSliceToMaps[T any](slice []T) ([]map[string]interface{}, error) {
	var result []map[string]interface{}

	for i, item := range slice {
		// Convert each item to JSON
		itemJSON, err := json.Marshal(item)
		if err != nil {
			return nil, fmt.Errorf("error marshalling item: %w", err)
		}

		// Convert JSON to map
		itemMap := make(map[string]interface{})
		err = json.Unmarshal(itemJSON, &itemMap)
		if err != nil {
			return nil, fmt.Errorf("error unmarshalling item JSON: %w", err)
		}

		// Add the sequential ID (starting from 1)
		itemMap["ID"] = i + 1

		// Append the map to the result slice
		result = append(result, itemMap)
	}

	return result, nil
}
