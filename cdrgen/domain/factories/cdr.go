package factories

import (
	"math/rand"
	"time"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

func getLastNearestStartInterval(t time.Time) time.Time {
	// Calculate minutes since the start of the day
	totalMinutes := t.Hour()*60 + t.Minute()

	// Round down to the nearest 30-minute interval
	intervalMinutes := totalMinutes / 30 * 30

	// Create a new time object with the rounded minutes
	return time.Date(t.Year(), t.Month(), t.Day(), intervalMinutes/60, intervalMinutes%60, 0, 0, t.Location())
}

// GenerateCdr generates a list of CDRs based on the input configuration.
func GenerateCdr(config map[string]interface{}) ([]*entities.Cdr, error) {
	var cdrs []*entities.Cdr

	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	startTime := config["startTime"].(time.Time)
	//	serviceTypes := config["serviceTypes"].([]entities.ServiceType) // List of entities.ServiceType

	// Generate CDRs for 10 intervals
	currentTime := startTime
	for i := 0; i < 10; i++ {

		// Create a new CDR
		cdr := &entities.Cdr{
			ID: rand.Intn(1000000), // Random ID for demo purposes
		}

		// Add to the list
		cdrs = append(cdrs, cdr)

		// Move to the next interval (30 minutes forward)
		currentTime = currentTime.Add(30 * time.Minute)
	}

	return cdrs, nil
}
