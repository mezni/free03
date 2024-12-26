package entities

// NetworkTechnology struct definition
type NetworkTechnology struct {
	ID          int
	Name        string
	Description string
}

// Factory function for NetworkTechnology
func NewNetworkTechnology(id int, name string, description string) NetworkTechnology {
	return NetworkTechnology{
		ID:          id,
		Name:        name,
		Description: description,
	}
}
