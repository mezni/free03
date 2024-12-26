package entities

type NetworkTechnology struct {
	ID          int
	Name        string
	Description string
}

func NetworkTechnologyFactory(id int, name, description string) *NetworkTechnology {
	return &NetworkTechnology{
		ID:          id,
		Name:        name,
		Description: description,
	}
}