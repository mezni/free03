package entities

import "github.com/google/uuid"

// NetworkTechnology represents a simple network technology.
type NetworkTechnology struct {
	ID          string
	Name        string
	Description string
}

// NetworkTechnologyFactory is a factory to create NetworkTechnology objects
type NetworkTechnologyFactory struct{}

// NewNetworkTechnology creates a new NetworkTechnology instance with the given name and description
func (f *NetworkTechnologyFactory) NewNetworkTechnology(name, description string) NetworkTechnology {
	return NetworkTechnology{
		ID:          uuid.New().String(),
		Name:        name,
		Description: description,
	}
}

func PredefinedNetworkTechnologies(factory *NetworkTechnologyFactory) []NetworkTechnology {
	return []NetworkTechnology{
		factory.NewNetworkTechnology("2G", "Second Generation Cellular Network"),
		factory.NewNetworkTechnology("3G", "Third Generation Cellular Network"),
		factory.NewNetworkTechnology("4G", "Fourth Generation Cellular Network"),
		factory.NewNetworkTechnology("5G", "Fifth Generation Cellular Network"),
	}
}
