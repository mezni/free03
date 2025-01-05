package factories

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"math/rand"
	"time"
)

// GenerateCustomers generates customers based on the provided configuration.
func GenerateCustomers(config *mappers.BusinessConfig) ([]*entities.Customer, error) {
	var customers []*entities.Customer

	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	// Generate customers for home MSISDN
	for i := 0; i < config.Customer.Msisdn.Home.Count; i++ {
		msisdn := generateMsisdn(config.Customer.Msisdn.Home.CountryCode, config.Customer.Msisdn.Home.NdcRanges, config.Customer.Msisdn.Home.Digits)
		customer := &entities.Customer{
			MSISDN:       msisdn,
			CustomerType: "Home", // For demonstration, this could be dynamic
		}
		customers = append(customers, customer)
	}

	// Generate customers for national MSISDN
	for i := 0; i < config.Customer.Msisdn.National.Count; i++ {
		msisdn := generateMsisdn(config.Customer.Msisdn.National.CountryCode, config.Customer.Msisdn.National.NdcRanges, config.Customer.Msisdn.National.Digits)
		customer := &entities.Customer{
			MSISDN:       msisdn,
			CustomerType: "National", // For demonstration, this could be dynamic
		}
		customers = append(customers, customer)
	}

	// Generate customers for international MSISDN
	for i := 0; i < config.Customer.Msisdn.International.Count; i++ {
		msisdn := generateMsisdnForInternational(config.Customer.Msisdn.International.Prefixes, config.Customer.Msisdn.International.Digits)
		customer := &entities.Customer{
			MSISDN:       msisdn,
			CustomerType: "International", // For demonstration, this could be dynamic
		}
		customers = append(customers, customer)
	}

	return customers, nil
}

// generateMsisdn generates a random MSISDN based on country code, NDC ranges, and digits.
func generateMsisdn(countryCode string, ndcRanges [][2]int, digits int) string {
	// Pick a random NDC range
	rangeIdx := rand.Intn(len(ndcRanges))
	ndc := rand.Intn(ndcRanges[rangeIdx][1]-ndcRanges[rangeIdx][0]) + ndcRanges[rangeIdx][0]

	// Generate the remaining digits
	remainingDigits := digits - len(fmt.Sprintf("%d", ndc))
	number := fmt.Sprintf("%d%0*d", ndc, remainingDigits, rand.Intn(int(1e6)))

	return countryCode + number
}

// generateMsisdnForInternational generates a random MSISDN for international numbers using prefixes and digits.
func generateMsisdnForInternational(prefixes []string, digits int) string {
	// Pick a random prefix
	prefix := prefixes[rand.Intn(len(prefixes))]

	// Generate the remaining digits
	remainingDigits := digits - len(prefix)
	number := fmt.Sprintf("%s%0*d", prefix, remainingDigits, rand.Intn(int(1e6)))

	return number
}
