package entities

// NetworkTechnology represents the network technology entity.
type Cdr struct {
	ID                  int
	CallID              int64
	TAC                 string
	LAC                 string
	CellID              string
	CallingPartyNumber  string
	CalledPartyNumber   string
	IMSI                string
	IMEI                string
	CallType            string
	CallReferenceNumber string
	PartialIndicator    bool
	CallStartTime       string
	CallEndTime         string
	CallDurationSec     int
	NetworkTechnology   string
}
