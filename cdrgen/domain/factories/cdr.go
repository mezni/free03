package factories

import (
	"math/rand"
	"time"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// GenerateCdr generates a list of CDRs based on the input configuration.
func GenerateCdr(config map[string]interface{}) ([]*entities.Cdr, error) {
	var cdrs []*entities.Cdr

	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	cdrIdSeq := config["cdrIdSeq"].(int64) // The initial cdrIdSeq
	startTime := config["startTime"].(time.Time)

	// Generate CDRs for 10 intervals
	currentTime := startTime
	for i := 0; i < 10; i++ {
		// Increment the cdrIdSeq for each new CDR to ensure unique IDs
		cdrIdSeq++

		// Create a new CDR
		cdr := &entities.Cdr{
			ID: cdrIdSeq, // Assign the incremented ID
		}

		// Add to the list
		cdrs = append(cdrs, cdr)

		// Move to the next interval (30 minutes forward)
		currentTime = currentTime.Add(30 * time.Minute)
	}

	return cdrs, nil
}
