package entities

// Location represents a single location entry
type Location struct {
	LocationID        int
	NetworkTechnology string
	Name              string
	LatitudeMin       float64
	LatitudeMax       float64
	LongitudeMin      float64
	LongitudeMax      float64
	AreaCode          int
}
