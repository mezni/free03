package entities

// NetworkTechnology represents the network technology entity.
type Customer struct {
	ID           int
	MSISDN       string
	IMSI         string
	IMEI         string
	CustomerType string
	AccountType  string
	Status       string
}
