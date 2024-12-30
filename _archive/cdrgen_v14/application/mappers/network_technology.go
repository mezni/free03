package mappers

import (
	"fmt"
	"strconv"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// Error definitions
var (
	ErrMissingID        = fmt.Errorf("missing ID field in the map")
	ErrInvalidID        = fmt.Errorf("invalid ID, must be a positive integer")
	ErrConversionID     = fmt.Errorf("unable to convert ID to an integer")
	ErrEmptyName        = fmt.Errorf("name cannot be empty")
	ErrEmptyDescription = fmt.Errorf("description cannot be empty")
)

// NetworkTechnologyMapper defines the struct for mapping NetworkTechnology entities.
type NetworkTechnologyMapper struct{}

// ToMap converts a NetworkTechnology instance to a map, with ID as a string.
func (m *NetworkTechnologyMapper) ToMap(n *entities.NetworkTechnology) map[string]interface{} {
	return map[string]interface{}{
		"ID":          strconv.Itoa(n.ID), // Convert ID to string
		"Name":        n.Name,
		"Description": n.Description,
	}
}

// FromMap converts a map to a NetworkTechnology instance, with ID as an integer.
func (m *NetworkTechnologyMapper) FromMap(data map[string]interface{}) (*entities.NetworkTechnology, error) {
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
			return nil, ErrConversionID
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
	if description == "" {
		return nil, ErrEmptyDescription
	}

	return &entities.NetworkTechnology{
		ID:          id,
		Name:        name,
		Description: description,
	}, nil
}

// ToListMap converts a slice of NetworkTechnology instances to a slice of maps, with ID as a string.
func (m *NetworkTechnologyMapper) ToListMap(networkTechnologies []*entities.NetworkTechnology) []map[string]interface{} {
	var result []map[string]interface{}
	for _, nt := range networkTechnologies {
		result = append(result, m.ToMap(nt))
	}
	return result
}

// FromListMap converts a slice of maps to a slice of NetworkTechnology instances, with ID as an integer.
func (m *NetworkTechnologyMapper) FromListMap(data []map[string]interface{}) ([]*entities.NetworkTechnology, error) {
	var result []*entities.NetworkTechnology
	for _, item := range data {
		nt, err := m.FromMap(item)
		if err != nil {
			return nil, err
		}
		result = append(result, nt)
	}
	return result, nil
}
