package entities

// Location represents a geographical location within the network.
type Location struct {
	ID                int
	Name              string
	LatitudeMin       float64
	LatitudeMax       float64
	LongitudeMin      float64
	LongitudeMax      float64
	AreaCode          int
	NetworkTechnology string
}
