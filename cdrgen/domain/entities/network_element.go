package entities

// NetworkElement represents a network element in the telecom system.
type NetworkElement struct {
	ID       string // Unique identifier for the network element
	Name     string // Name of the network element
	Location string // Physical or logical location
	Type     string // e.g., "BTS", "MSC", "Router"
}
