package entities

// NetworkTechnology represents the network technology entity.
type Cdr struct {
	ID                int
	ServiceType       string
	TAC               string
	LAC               string
	CellID            string
	NetworkTechnology string
	MessageLength     int
	DeliveryStatus    string
	Reference         string
	StartTime         string
	EndTime           string
	Duration          int
}
