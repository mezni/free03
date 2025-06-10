package factories

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"math/rand"
	"time"
	// "strconv"
)

// GenerateCustomers generates customers based on the provided configuration.
func GenerateCustomers(config *mappers.BusinessConfig) ([]*entities.Customer, error) {
	var customers []*entities.Customer

	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	// Generate customers for home MSISDN
	for i := 0; i < config.Customer.Msisdn.Home.Count; i++ {
		msisdn := generateMsisdn(config.Customer.Msisdn.Home.CountryCode, config.Customer.Msisdn.Home.NdcRanges, config.Customer.Msisdn.Home.Digits)
		imsi := generateRandomNumber(15)
		imei := generateRandomNumber(15)
		customer := &entities.Customer{
			MSISDN:       msisdn,
			IMSI:         imsi,
			IMEI:         imei,
			CustomerType: "Home",
			AccountType:  "Postpaid",
			Status:       "Active",
		}
		customers = append(customers, customer)
	}

	// Generate customers for national MSISDN
	for i := 0; i < config.Customer.Msisdn.National.Count; i++ {
		msisdn := generateMsisdn(config.Customer.Msisdn.National.CountryCode, config.Customer.Msisdn.National.NdcRanges, config.Customer.Msisdn.National.Digits)
		imsi := generateRandomNumber(15)
		imei := generateRandomNumber(15)
		customer := &entities.Customer{
			MSISDN:       msisdn,
			IMSI:         imsi,
			IMEI:         imei,
			CustomerType: "National",
			AccountType:  "Postpaid",
			Status:       "Active",
		}
		customers = append(customers, customer)
	}

	// Generate customers for international MSISDN
	for i := 0; i < config.Customer.Msisdn.International.Count; i++ {
		msisdn := generateMsisdnForInternational(config.Customer.Msisdn.International.Prefixes, config.Customer.Msisdn.International.Digits)
		imsi := generateRandomNumber(15)
		imei := generateRandomNumber(15)
		customer := &entities.Customer{
			MSISDN:       msisdn,
			IMSI:         imsi,
			IMEI:         imei,
			CustomerType: "International",
			AccountType:  "Postpaid",
			Status:       "Active",
		}
		customers = append(customers, customer)
	}

	return customers, nil
}

// generateMsisdn generates a random MSISDN based on country code, NDC ranges, and digits from the config.
func generateMsisdn(countryCode string, ndcRanges [][2]int, digits int) string {
	// Pick a random NDC range
	rangeIdx := rand.Intn(len(ndcRanges))
	ndc := rand.Intn(ndcRanges[rangeIdx][1]-ndcRanges[rangeIdx][0]) + ndcRanges[rangeIdx][0]

	number := fmt.Sprintf("%d%0*d", ndc, digits, rand.Intn(int(1e6)))

	// Return the full MSISDN including country code and random number
	return countryCode + number
}

// generateMsisdnForInternational generates a random MSISDN for international numbers using prefixes and digits from the config.
func generateMsisdnForInternational(prefixes []string, digits int) string {
	// Pick a random prefix
	prefix := prefixes[rand.Intn(len(prefixes))]

	number := fmt.Sprintf("%s%0*d", prefix, digits, rand.Intn(int(1e6)))

	// Return the full MSISDN for international number
	return number
}

// generateRandomNumber generates a random number based on the provided digits length.
func generateRandomNumber(digits int) string {
	// Generate a random number of specified digits length
	// Ensure the random number length matches the 'digits' parameter
	upperLimit := int64(1)
	for i := 0; i < digits; i++ {
		upperLimit *= 10
	}

	// Random number within the range
	randomNumber := rand.Int63n(upperLimit)

	// Format the random number to be exactly 'digits' long
	return fmt.Sprintf(fmt.Sprintf("%%0%dd", digits), randomNumber)
}
