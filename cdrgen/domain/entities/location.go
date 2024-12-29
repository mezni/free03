package entities

// Location represents a geographical location with various details.
type Location struct {
	ID                int     `json:"id"`
	NetworkTechnology string  `json:"network_technology"`
	Name              string  `json:"name"`
	LatitudeMin       float64 `json:"latitude_min"`
	LatitudeMax       float64 `json:"latitude_max"`
	LongitudeMin      float64 `json:"longitude_min"`
	LongitudeMax      float64 `json:"longitude_max"`
	AreaCode          int     `json:"area_code"`
}

// NewLocation creates a new Location instance.
func NewLocation(id int, networkTechnology, name string, latMin, latMax, longMin, longMax float64, areaCode int) (*Location, error) {
	location := &Location{
		ID:                id,
		NetworkTechnology: networkTechnology,
		Name:              name,
		LatitudeMin:       latMin,
		LatitudeMax:       latMax,
		LongitudeMin:      longMin,
		LongitudeMax:      longMax,
		AreaCode:          areaCode,
	}
	// You can add any additional validation or initialization logic here if needed
	return location, nil
}
