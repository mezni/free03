package factories

import (
	"math/rand"
	"time"
	"fmt"
	"log"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

func GetRandomServiceType(technology string, name string, serviceTypes []entities.ServiceType) (*entities.ServiceType, error) {
	// Filter service types based on the provided technology and name
	var matchingServiceTypes []entities.ServiceType
	for _, serviceType := range serviceTypes {
		if serviceType.NetworkTechnology == technology && serviceType.Name == name {
			matchingServiceTypes = append(matchingServiceTypes, serviceType)
		}
	}

	// Check if any matching service types were found
	if len(matchingServiceTypes) == 0 {
		return nil, fmt.Errorf("no service types found with NetworkTechnology '%s' and Name '%s'", technology, name)
	}

	// Select a random service type from the matching list
	randomIndex := rand.Intn(len(matchingServiceTypes))
	selectedServiceType := matchingServiceTypes[randomIndex]

	return &selectedServiceType, nil
}

// GenerateCdr generates a list of CDRs based on the input configuration.
func GenerateCdr(config map[string]interface{}) ([]*entities.Cdr, error) {
	var cdrs []*entities.Cdr

	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	cdrIdSeq := config["cdrIdSeq"].(int64) // The initial cdrIdSeq
	startTime := config["startTime"].(time.Time)

serviceTypes := []entities.ServiceType{ /* populate this slice with your data */ }



	// Generate CDRs for 10 intervals
	currentTime := startTime
	for i := 0; i < 10; i++ {
		// Increment the cdrIdSeq for each new CDR to ensure unique IDs
		cdrIdSeq++


		randomService, err := GetRandomServiceType( "2G", "Voice Call",serviceTypes)
		if err != nil {
			log.Printf("Error while getting random service: %v", err)
			continue // Skip this iteration if there's an error
		}

		// Create a new CDR
		cdr := &entities.Cdr{
			ID:               cdrIdSeq,
			ServiceTypeName:  randomService.Name,
			NetworkTechnology: randomService.NetworkTechnology,
		}

		// Add to the list of CDRs
		cdrs = append(cdrs, cdr)

		// Move to the next interval (30 minutes forward)
		currentTime = currentTime.Add(30 * time.Minute)
	}

	return cdrs, nil
}

