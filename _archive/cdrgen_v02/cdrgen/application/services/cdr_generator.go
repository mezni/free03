package services

import (
	"database/sql"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
	"log"
	"math/rand"
	"sync/atomic"
	"time"
)

type CdrGeneratorService struct {
	DB                           *sql.DB
	NetworkTechSqliteRepo        *sqlitestore.NetworkTechnologyRepository
	NetworkElementTypeSqliteRepo *sqlitestore.NetworkElementTypeRepository
	ServiceTypeSqliteRepo        *sqlitestore.ServiceTypeRepository
	ServiceNodeSqliteRepo        *sqlitestore.ServiceNodeRepository
	LocationSqliteRepo           *sqlitestore.LocationRepository
	NetworkElementSqliteRepo     *sqlitestore.NetworkElementRepository
	CustomerSqliteRepo           *sqlitestore.CustomerRepository
	NetworkTechInmemRepo         *inmemstore.InMemNetworkTechnologyRepository
	NetworkElementInmemRepo      *inmemstore.InMemNetworkElementRepository
	ServiceTypeInmemRepo         *inmemstore.InMemServiceTypeRepository
	CustomerInmemRepo            *inmemstore.InMemCustomerRepository
}

var cdrId int32

// Pre-seed random number generator
func init() {
	rand.Seed(time.Now().UnixNano())
}

// NewCdrGeneratorService initializes the CdrGeneratorService with all repositories.
func NewCdrGeneratorService(dbFile string) (*CdrGeneratorService, error) {
	db, err := sql.Open("sqlite3", dbFile)
	if err != nil {
		return nil, fmt.Errorf("could not open database: %v", err)
	}

	if err := db.Ping(); err != nil {
		db.Close()
		return nil, fmt.Errorf("could not connect to database: %v", err)
	}

	return &CdrGeneratorService{
		DB:                           db,
		NetworkTechSqliteRepo:        sqlitestore.NewNetworkTechnologyRepository(db),
		NetworkElementTypeSqliteRepo: sqlitestore.NewNetworkElementTypeRepository(db),
		ServiceTypeSqliteRepo:        sqlitestore.NewServiceTypeRepository(db),
		ServiceNodeSqliteRepo:        sqlitestore.NewServiceNodeRepository(db),
		LocationSqliteRepo:           sqlitestore.NewLocationRepository(db),
		NetworkElementSqliteRepo:     sqlitestore.NewNetworkElementRepository(db),
		CustomerSqliteRepo:           sqlitestore.NewCustomerRepository(db),
		NetworkTechInmemRepo:         inmemstore.NewInMemNetworkTechnologyRepository(),
		NetworkElementInmemRepo:      inmemstore.NewInMemNetworkElementRepository(),
		ServiceTypeInmemRepo:         inmemstore.NewInMemServiceTypeRepository(),
		CustomerInmemRepo:            inmemstore.NewInMemCustomerRepository(),
	}, nil
}

func (c *CdrGeneratorService) SetupCache() error {
	// Fetch and cache network technologies, elements, service types, and customers
	networkTechnologies, err := c.NetworkTechSqliteRepo.GetAll()
	if err != nil {
		return fmt.Errorf("failed to fetch network technologies: %v", err)
	}
	for _, tech := range networkTechnologies {
		if err := c.NetworkTechInmemRepo.Insert(tech); err != nil {
			log.Printf("Warning: failed to insert network technology ID %d: %v", tech.ID, err)
		}
	}

	networkElements, err := c.NetworkElementSqliteRepo.GetAll()
	if err != nil {
		return fmt.Errorf("failed to fetch network elements: %v", err)
	}
	for _, ne := range networkElements {
		if err := c.NetworkElementInmemRepo.Insert(ne); err != nil {
			log.Printf("Warning: failed to insert network element ID %d: %v", ne.ID, err)
		}
	}

	serviceTypes, err := c.ServiceTypeSqliteRepo.GetAll()
	if err != nil {
		return fmt.Errorf("failed to fetch service types: %v", err)
	}
	for _, st := range serviceTypes {
		if err := c.ServiceTypeInmemRepo.Insert(st); err != nil {
			log.Printf("Warning: failed to insert service type ID %d: %v", st.ID, err)
		}
	}

	customers, err := c.CustomerSqliteRepo.GetAll()
	if err != nil {
		return fmt.Errorf("failed to fetch customers: %v", err)
	}
	for _, cs := range customers {
		if err := c.CustomerInmemRepo.Insert(cs); err != nil {
			log.Printf("Warning: failed to insert customer ID %d: %v", cs.ID, err)
		}
	}

	log.Println("Cache setup complete.")
	return nil
}

// GetNextCdrID returns a unique, thread-safe CDR ID.
func getNextCdrID() int {
	return int(atomic.AddInt32(&cdrId, 1))
}

func RandomNetwork(twoGProb, threeGProb, fourGProb float64) string {
	randomNumber := rand.Float64()

	if randomNumber < twoGProb {
		return "2G"
	} else if randomNumber < twoGProb+threeGProb {
		return "3G"
	} else if randomNumber < twoGProb+threeGProb+fourGProb {
		return "4G"
	} else {
		return "5G"
	}
}

func GetRandomCustomerType(customerTypes []string, customerProbabilities []float64) (string, error) {
	if len(customerTypes) != len(customerProbabilities) {
		return "", fmt.Errorf("customerTypes and customerProbabilities must have the same length")
	}

	cumulativeProbabilities := make([]float64, len(customerProbabilities))
	cumulativeSum := 0.0
	for i, prob := range customerProbabilities {
		cumulativeSum += prob
		cumulativeProbabilities[i] = cumulativeSum
	}

	// Validate that probabilities sum to 1
	if cumulativeSum < 0.99 || cumulativeSum > 1.01 {
		return "", fmt.Errorf("customerProbabilities must sum to 1, got %f", cumulativeSum)
	}

	// Select customer type based on random number
	randomNumber := rand.Float64()
	for i, cumProb := range cumulativeProbabilities {
		if randomNumber <= cumProb {
			return customerTypes[i], nil
		}
	}
	return "", fmt.Errorf("failed to select customer type")
}

func (c *CdrGeneratorService) GetCustomers(callingCustomerType, calledCustomerType string) (entities.Customer, entities.Customer, error) {
	// Fetch a random customer for the calling party
	callingCustomerPtr, err := c.CustomerInmemRepo.GetRandomByCustomerType(callingCustomerType)
	if err != nil {
		return entities.Customer{}, entities.Customer{}, fmt.Errorf("failed to fetch calling customer: %v", err)
	}
	callingCustomer := *callingCustomerPtr

	var calledCustomer entities.Customer

	// Fetch a random customer for the called party, ensuring it's different from the calling customer
	for {
		calledCustomerPtr, err := c.CustomerInmemRepo.GetRandomByCustomerType(calledCustomerType)
		if err != nil {
			return entities.Customer{}, entities.Customer{}, fmt.Errorf("failed to fetch called customer: %v", err)
		}
		calledCustomer = *calledCustomerPtr

		if calledCustomer.ID != callingCustomer.ID {
			break
		}
	}

	return callingCustomer, calledCustomer, nil
}

func GetStartOfInterval(inputTime time.Time) time.Time {
	// Calculate the start of the 30-minute interval
	hour := inputTime.Hour()
	minute := inputTime.Minute()

	intervalStartMinute := (minute / 30) * 30

	return time.Date(inputTime.Year(), inputTime.Month(), inputTime.Day(), hour, intervalStartMinute, 0, 0, inputTime.Location())
}

func GetRandomTimeInInterval(startOfInterval time.Time) time.Time {
	// Calculate the end of the interval
	endOfInterval := startOfInterval.Add(30 * time.Minute)
	randomDuration := time.Duration(rand.Int63n(int64(endOfInterval.Sub(startOfInterval))))

	return startOfInterval.Add(randomDuration)
}

func GetCallDurationSec() int {
	// Generate a random call duration
	randomChoice := rand.Float64()

	if randomChoice < 0.80 {
		return rand.Intn(600) + 1 // 80% chance for a number between 1 and 600
	} else if randomChoice < 0.85 {
		return 0 // 5% chance for 0
	} else {
		return rand.Intn(3000) + 601 // 15% chance for a number between 601 and 3600
	}
}

func GetCallIntervals(callStartTime, callEndTime, intervalStartTime, intervalEndTime time.Time) ([]map[string]interface{}, error) {
	var intervals []map[string]interface{}

	// If the call ends before the interval starts, there's no need to process it
	if callEndTime.Before(intervalStartTime) {
		return intervals, nil
	}

	// Recursive case: Generate intervals for the call
	currentStartTime := callStartTime
	currentEndTime := intervalEndTime

	for currentStartTime.Before(callEndTime) {
		if currentStartTime.Before(intervalStartTime) {
			currentStartTime = intervalStartTime
		}

		// If the call ends within the current 30-minute interval, adjust the end time
		if currentEndTime.After(callEndTime) {
			currentEndTime = callEndTime
		}

		// Add current interval details to the list
		intervals = append(intervals, map[string]interface{}{
			"start":    currentStartTime.Format("2006-01-02 15:04:05"),
			"end":      currentEndTime.Format("2006-01-02 15:04:05"),
			"duration": int(currentEndTime.Sub(currentStartTime).Seconds()),
		})

		// If the call has reached the end, exit the loop
		if currentEndTime.Equal(callEndTime) {
			break
		}

		// Move to the next interval (next 30-minute period)
		currentStartTime = currentEndTime
		currentEndTime = currentEndTime.Add(30 * time.Minute)
	}

	return intervals, nil
}

func (c *CdrGeneratorService) Generate() error {
	// Setup the cache
	if err := c.SetupCache(); err != nil {
		return fmt.Errorf("failed to set up cache: %v", err)
	}

	currentTime := time.Now()
	startOfInterval := GetStartOfInterval(currentTime)
	intervalEndTime := startOfInterval.Add(30 * time.Minute)

	// Randomly select a network technology
	networkTechnology := RandomNetwork(0.05, 0.4, 0.55)

	customerTypes := []string{"Home", "National", "International"}
	callerProbabilities := []float64{0.75, 0.2, 0.05}
	calleeProbabilities := []float64{0.55, 0.4, 0.05}

	callerType, err := GetRandomCustomerType(customerTypes, callerProbabilities)
	if err != nil {
		return fmt.Errorf("failed to get caller customer type: %v", err)
	}

	calleeType, err := GetRandomCustomerType(customerTypes, calleeProbabilities)
	if err != nil {
		return fmt.Errorf("failed to get callee customer type: %v", err)
	}

	var callType string
	if callerType == "Home" && calleeType == "Home" {
		callType = "Local"
	} else {
		callType = "Other"
	}

	// Get two different customers
	callingCustomer, calledCustomer, err := c.GetCustomers(callerType, calleeType)
	if err != nil {
		return fmt.Errorf("failed to get two different customers: %v", err)
	}

	callStartTime := GetRandomTimeInInterval(startOfInterval)
	callDurationSec := GetCallDurationSec()

	// Calculate callEndTime
	callEndTime := callStartTime.Add(time.Duration(callDurationSec) * time.Second)

	intervals, err := GetCallIntervals(callStartTime, callEndTime, startOfInterval, intervalEndTime)
	if err != nil {
		return fmt.Errorf("error in calculating call intervals: %v", err)
	}

	if len(intervals) == 1 {
		// Single CDR generation
		cdrId := getNextCdrID()
		cdr := &entities.Cdr{
			ID:                  cdrId,
			CallingPartyNumber:  callingCustomer.MSISDN,
			CalledPartyNumber:   calledCustomer.MSISDN,
			IMSI:                callingCustomer.IMSI,
			IMEI:                calledCustomer.IMEI,
			CallType:            callType,
			CallReferenceNumber: fmt.Sprintf("REF-%d", cdrId),
			PartialIndicator:    false,
			CallStartTime:       callStartTime.Format("2006-01-02 15:04:05"),
			CallEndTime:         callEndTime.Format("2006-01-02 15:04:05"),
			CallDurationSec:     callDurationSec,
			NetworkTechnology:   networkTechnology,
		}
		log.Printf("Generated CDR: %+v", cdr)
	} else {

		for i, interval := range intervals {
			intervalStartTime, err := time.Parse("2006-01-02 15:04:05", interval["start"].(string))
			if err != nil {
				return fmt.Errorf("error parsing start time: %v", err)
			}
			intervalEndTime, err := time.Parse("2006-01-02 15:04:05", interval["end"].(string))
			if err != nil {
				return fmt.Errorf("error parsing end time: %v", err)
			}

			// Generate CDR ID and call reference number only for the first interval
			cdrId := getNextCdrID()
			var callReferenceNumber string
			if i == 0 {
				callReferenceNumber = fmt.Sprintf("REF-%d", cdrId)
			}

			// Create the CDR for the current interval
			cdr := &entities.Cdr{
				ID:                  cdrId,
				CallingPartyNumber:  callingCustomer.MSISDN,
				CalledPartyNumber:   calledCustomer.MSISDN,
				IMSI:                callingCustomer.IMSI,
				IMEI:                calledCustomer.IMEI,
				CallType:            callType,
				CallReferenceNumber: callReferenceNumber, // Same reference for the whole call
				PartialIndicator:    true,
				CallStartTime:       intervalStartTime.Format("2006-01-02 15:04:05"),
				CallEndTime:         intervalEndTime.Format("2006-01-02 15:04:05"),
				CallDurationSec:     interval["duration"].(int),
				NetworkTechnology:   networkTechnology,
			}
			log.Printf("Generated Partial CDR: %+v", cdr)
		}

	}

	return nil
}
