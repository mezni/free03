package entities

import (
	"strconv"
)

// NetworkTechnology represents a network technology.
type NetworkTechnology struct {
	ID          int
	Name        string
	Description string
}

// ToMap converts a NetworkTechnology instance to a map, with ID as a string.
func (n *NetworkTechnology) ToMap() map[string]interface{} {
	return map[string]interface{}{
		"ID":          strconv.Itoa(n.ID), // Convert ID to string
		"Name":        n.Name,
		"Description": n.Description,
	}
}

// FromMap converts a map to a NetworkTechnology instance, with ID as an integer.
func FromMap(data map[string]interface{}) (*NetworkTechnology, error) {
	// Extract ID from the map and ensure it's a valid integer
	idValue, ok := data["ID"]
	if !ok {
		return nil, ErrMissingID
	}

	var id int
	switch v := idValue.(type) {
	case string:
		// If ID is a string, try to convert it to an integer
		parsedID, err := strconv.Atoi(v)
		if err != nil {
			return nil, ErrConverstionID
		}
		id = parsedID
	case int:
		// If it's already an integer, use it directly
		id = v
	default:
		return nil, ErrInvalidID
	}

	// Ensure ID is a positive integer
	if id <= 0 {
		return nil, ErrInvalidID
	}

	// Extract Name and Description
	name, _ := data["Name"].(string)
	if name == "" {
		return nil, ErrEmptyName
	}
	description, _ := data["Description"].(string)

	return &NetworkTechnology{
		ID:          id,
		Name:        name,
		Description: description,
	}, nil
}
