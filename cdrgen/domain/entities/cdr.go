package entities

import "time"

// CDR represents a Call Detail Record.
type CDR struct {
	ID        string
	Caller    string
	Callee    string
	Duration  int // seconds
	Timestamp time.Time
	CallType  string // e.g., "incoming", "outgoing"
}
