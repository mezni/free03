package entities

// NetworkElement represents the network element type entity.
type NetworkElement struct {
	ID                int
	Name              string
	Description       string
	NetworkTechnology string
	IPAddress         string
	Status            string
	TAC               *string
	LAC               *string
	CellID            *string
}
