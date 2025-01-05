package main

import (
	"fmt"
	"math/rand"
	"time"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// Sequence generates a sequence of int64 integers starting from the given value.
func Sequence(start int64) func() int64 {
	counter := start
	return func() int64 {
		result := counter
		counter++
		return result
	}
}

func GetSeqCurrent() int64 {
	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	// Generate a random two-digit number
	randomPrefix := rand.Intn(90) + 10

	// Get the trimmed Unix millisecond timestamp
	trimmedTimestamp := time.Now().UnixMilli() % 1e9 // Removes the first 4 digits

	// Combine the random prefix and trimmed timestamp, adjusting for the prefix's place value
	return int64(randomPrefix)*1e9 + trimmedTimestamp
}

func main() {
	// Create the sequence generator
	cdrId := Sequence(GetSeqCurrent())

	// Initialize an array to hold 10 CDRs
	cdrs := make([]entities.Cdr, 10)

	// Generate 10 CDRs with unique IDs
	for i := 0; i < 10; i++ {
		cdrs[i] = entities.Cdr{
			ID:                 cdrId(),
			CallingPartyNumber: fmt.Sprintf("+2165413535%d", i),
			CalledPartyNumber:  fmt.Sprintf("+2165050505%d", i),
			CallStartTime:      "2025-01-05 14:30:00",
			CallEndTime:        "2025-01-05 14:35:00",
			CallDuration:       300,
		}
	}

	// Print the array of CDRs
	for _, cdr := range cdrs {
		fmt.Println(cdr)
	}
}
