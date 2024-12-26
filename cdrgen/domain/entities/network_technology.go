package entities

type NetworkTechnology struct {
	ID          int
	Name        string
	Description string
}

func NetworkTechnologyFactory(id int, name, description string) *NetworkTechnology {
	if id <= 0 {
		return nil, errors.New("invalid id")
	}
	if name == "" {
		return nil, errors.New("invalid name")
	}
	return &NetworkTechnology{
		ID:          id,
		Name:        name,
		Description: description,
	}
}