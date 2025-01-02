package entities

// Customer represents a telecom customer.
type Customer struct {
	ID     string // Unique customer ID
	MSISDN string // Mobile Station ISDN number
	IMSI   string // International Mobile Subscriber Identity
	IMEI   string // International Mobile Equipment Identity
}
