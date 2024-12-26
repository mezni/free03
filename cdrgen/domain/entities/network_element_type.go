package entities

// NetworkElementType struct definition
type NetworkElementType struct {
	ID                    int
	Name                  string
	Description           string
	NetworkTechnologyName string
}

// Factory function for NetworkElementType
func NewNetworkElementType(id int, name string, description string, techName string) NetworkElementType {
	return NetworkElementType{
		ID:                    id,
		Name:                  name,
		Description:           description,
		NetworkTechnologyName: techName,
	}
}
