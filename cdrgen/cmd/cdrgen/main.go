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

// GetSeqCurrent generates a random timestamp-like value (int64) with a random prefix.
func GetSeqCurrent() int64 {
	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	// Generate a random two-digit number (for the prefix)
	randomPrefix := rand.Intn(90) + 10 // Ensures a number between 10 and 99

	// Get the trimmed Unix millisecond timestamp (removes first 4 digits)
	trimmedTimestamp := time.Now().UnixMilli() % 1e9

	// Combine the random prefix and trimmed timestamp
	return int64(randomPrefix)*1e9 + trimmedTimestamp
}

// GenerateCallDuration returns a random call duration based on the specified probabilities.
func GenerateCallDuration() int {
	rand.Seed(time.Now().UnixNano())

	// Generate a random number between 0 and 100 to simulate probabilities
	probability := rand.Intn(100)

	if probability < 5 {
		// 5% probability for 0 seconds
		return 0
	} else if probability < 10 {
		// 5% probability for a random duration between 601 and 3600 seconds (1 hour)
		return rand.Intn(3000) + 601 // Random number between 601 and 3600
	} else {
		// 90% probability for a random duration between 1 and 600 seconds
		return rand.Intn(600) + 1 // Random number between 1 and 600
	}
}

// RoundTimeToLast30Min rounds a given time to the last 30-minute interval.
func RoundTimeToLast30Min(t time.Time) time.Time {
	// Get the minutes of the current time
	minutes := t.Minute()

	// Calculate the number of minutes to subtract to get to the previous 30-minute mark
	var roundMinutes int
	if minutes < 30 {
		roundMinutes = minutes
	} else {
		roundMinutes = minutes - 30
	}

	// Subtract the roundMinutes from the current time
	roundedTime := t.Add(-time.Minute * time.Duration(roundMinutes))

	// Set seconds and nanoseconds to zero for precision
	return time.Date(roundedTime.Year(), roundedTime.Month(), roundedTime.Day(), roundedTime.Hour(), roundedTime.Minute(), 0, 0, roundedTime.Location())
}

// GenerateCallEndTime generates a random CallEndTime between endTimeDump and endTimeDump-30 minutes.
func GenerateCallEndTime(endTimeDump time.Time) time.Time {
	// Generate a random number of minutes to subtract (between 0 and 30)
	randomMinutes := rand.Intn(31) // Random number between 0 and 30 minutes

	// Subtract the random minutes from endTimeDump
	callEndTime := endTimeDump.Add(-time.Minute * time.Duration(randomMinutes))

	return callEndTime
}

// GenerateCallStartTime calculates CallStartTime by subtracting the CallDuration from the CallEndTime.
func GenerateCallStartTime(callEndTime time.Time, callDuration int) time.Time {
	// Convert CallDuration from seconds to time.Duration and subtract from CallEndTime
	callStartTime := callEndTime.Add(-time.Second * time.Duration(callDuration))

	return callStartTime
}

// GenerateCallDetails generates a list of CallStartTime, CallEndTime, and CallDuration.
func GenerateCallDetails(endTimeDump time.Time, numCalls int) []entities.Cdr {
	var cdrs []entities.Cdr

	for i := 0; i < numCalls; i++ {
		// Generate a random CallEndTime between endTimeDump and endTimeDump-30 minutes
		callEndTime := GenerateCallEndTime(endTimeDump)

		// Generate a random CallDuration
		callDuration := GenerateCallDuration()

		// Generate CallStartTime as CallEndTime - CallDuration
		callStartTime := GenerateCallStartTime(callEndTime, callDuration)

		// Check if CallStartTime is earlier than endTimeDump - 30 minutes
		if callStartTime.Before(endTimeDump.Add(-30 * time.Minute)) {
			// Create two CDRs

			// First CDR starts from endTimeDump - 30 minutes
			firstCallStartTime := endTimeDump.Add(-30 * time.Minute)
			firstCallEndTime := firstCallStartTime.Add(time.Second * time.Duration(callDuration))

			// Add the first CDR
			cdrs = append(cdrs, entities.Cdr{
				CallStartTime: firstCallStartTime.Format("2006-01-02 15:04:05"),
				CallEndTime:   firstCallEndTime.Format("2006-01-02 15:04:05"),
				CallDuration:  callDuration,
			})

			// Second CDR starts from the first CDR's end time
			secondCallStartTime := firstCallEndTime
			secondCallEndTime := secondCallStartTime.Add(time.Second * time.Duration(callDuration))

			// Add the second CDR
			cdrs = append(cdrs, entities.Cdr{
				CallStartTime: secondCallStartTime.Format("2006-01-02 15:04:05"),
				CallEndTime:   secondCallEndTime.Format("2006-01-02 15:04:05"),
				CallDuration:  callDuration,
			})
		} else {
			// If the start time is after endTimeDump - 30 minutes, add a single CDR
			cdrs = append(cdrs, entities.Cdr{
				CallStartTime: callStartTime.Format("2006-01-02 15:04:05"),
				CallEndTime:   callEndTime.Format("2006-01-02 15:04:05"),
				CallDuration:  callDuration,
			})
		}
	}

	return cdrs
}

func main() {
	// Create the sequence generator
	cdrId := Sequence(GetSeqCurrent())

	// Get the current time
	currentTime := time.Now()

	// Round the current time to the last 30-minute mark
	endTimeDump := RoundTimeToLast30Min(currentTime)

	// Generate a list of 10 CDRs
	cdrs := GenerateCallDetails(endTimeDump, 10)

	// Assign IDs to each CDR
	for i := 0; i < len(cdrs); i++ {
		cdrs[i].ID = cdrId()
		cdrs[i].CallingPartyNumber = fmt.Sprintf("+2165413535%d", i)
		cdrs[i].CalledPartyNumber = fmt.Sprintf("+2165050505%d", i)
	}

	// Print the array of CDRs
	for _, cdr := range cdrs {
		fmt.Println(cdr)
	}
}
