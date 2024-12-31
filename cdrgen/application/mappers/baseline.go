package mappers

import (
	"encoding/json"
	"errors"
)

var (
	ErrFailedToMarshal   = errors.New("failed to marshal map to byte data")
)


// mapToStruct helps to decode a map[string]interface{} into a target struct
func MapToStruct(data map[string]interface{}, result interface{}) error {
	// Marshal the map into JSON (which is []byte), then unmarshal into the target struct
	byteData, err := json.Marshal(data)
	if err != nil {
		return ErrFailedToMarshal
	}
	return json.Unmarshal(byteData, result)
}
