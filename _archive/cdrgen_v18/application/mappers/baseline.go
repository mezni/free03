package mappers

import (
	"encoding/json"
	"errors"
	"strconv"
	"reflect"
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

// MapToEntity is a generic function that maps a map[string]interface{} to an entity.
func MapToEntity[T any](data map[string]interface{}, entity *T) error {
	// Ensure the entity is a pointer to a struct
	typ := reflect.TypeOf(entity)
	if typ.Kind() != reflect.Ptr || typ.Elem().Kind() != reflect.Struct {
		return errors.New("entity must be a pointer to a struct")
	}

	// Get the value of the entity
	val := reflect.ValueOf(entity).Elem()

	// Iterate over the struct fields
	for i := 0; i < val.NumField(); i++ {
		field := val.Field(i)
		fieldName := val.Type().Field(i).Name
		fieldValue, exists := data[fieldName]

		// If the field exists in the map, set its value
		if exists {
			// Handle the "ID" field specifically to ensure it's an int
			if fieldName == "ID" {
				switch v := fieldValue.(type) {
				case string:
					// Try converting string to int
					id, err := strconv.Atoi(v)
					if err != nil {
						return errors.New("failed to convert ID to int")
					}
					field.Set(reflect.ValueOf(id))
				case float64:
					// If ID is already a float64, it may be a JSON number, so convert it to int
					field.Set(reflect.ValueOf(int(v)))
				default:
					// For unsupported types, return an error
					return errors.New("invalid type for ID field")
				}
			} else {
				// For other fields, just set the value directly
				field.Set(reflect.ValueOf(fieldValue))
			}
		} else {
			// Handle the case where the field does not exist in the map
			return errors.New("missing required field: " + fieldName)
		}
	}

	return nil
}
