package entities

type NetworkElementType struct {
	ID                  int
	Name                string
	Description         string
	NetworkTechnologyID string
}

func NetworkElementTypeFactory(id int, name, description,networknechnologyid string) *NetworkElementType {
    
	return &NetworkElementType{
		ID:          id,
		Name:        name,
		Description: description,
		NetworkTechnologyID: networknechnologyid,
	}
}