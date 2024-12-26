package entities

import "your_project/errors" // Import the errors package

// NetworkTechnology represents a type of network technology with ID, name, and description.
type NetworkTechnology struct {
	ID          int    // Unique identifier
	Name        string // Name of the technology
	Description string // Description of the technology (can be empty)
}

// NewNetworkTechnology creates and initializes a NetworkTechnology instance.
// Returns an error if the provided ID is non-positive or if the name is empty.
func NewNetworkTechnology(id int, name string, description string) (*NetworkTechnology, error) {
	if id <= 0 {
		return nil, errors.ErrInvalidID
	}
	if name == "" {
		return nil, errors.ErrEmptyName
	}

	return &NetworkTechnology{
		ID:          id,
		Name:        name,
		Description: description, // Description can be empty
	}, nil
}
