package entities

import "github.com/mezni/wovoka/cdrgen/domain/entities/errors"

// NetworkElementType represents a type of network element with ID, name, description, and technology name.
type NetworkElementType struct {
	ID                    int    // Unique identifier
	Name                  string // Name of the network element type
	Description           string // Description of the network element type (can be empty)
	NetworkTechnologyName string // The associated network technology's name (cannot be empty)
}

// NewNetworkElementType creates and initializes a NetworkElementType instance.
// Returns an error if the provided ID is non-positive, name is empty, or techName is empty.
func NewNetworkElementType(id int, name string, description string, techName string) (*NetworkElementType, error) {
	if id <= 0 {
		return nil, errors.ErrInvalidID
	}
	if name == "" {
		return nil, errors.ErrEmptyName
	}
	if techName == "" {
		return nil, errors.ErrEmptyTechName
	}

	return &NetworkElementType{
		ID:                    id,
		Name:                  name,
		Description:           description, // Description can be empty
		NetworkTechnologyName: techName,
	}, nil
}
