package entities

type Cdr struct {
	ID                 int64
	CallingPartyNumber string
	CalledPartyNumber  string
	CallStartTime      string
	CallEndTime        string
	CallDuration       int
}
