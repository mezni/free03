package entities

// NetworkTechnology represents the network technology entity.
type Cdr struct {
	ID                  int
	CallID              int64
	CallingPartyNumber  string
	CalledPartyNumber   string
	IMSI                string
	IMEI                string
	CallType            string
	CallReferenceNumber string
	PartialIndicator    bool
	NetworkTechnology   string
}
