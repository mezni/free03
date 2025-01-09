package services

import (
	"database/sql"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
	"log"
	"math/rand"
	"strconv"
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
	CdrInmemRepo                 *inmemstore.InMemCdrRepository
}

var cdrId int32

func init() {
	rand.Seed(time.Now().UnixNano()) // Pre-seed random number generator
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
		CdrInmemRepo:                 inmemstore.NewInMemCdrRepository(),
	}, nil
}

// SetupCache preloads data from SQLite into in-memory repositories.
func (c *CdrGeneratorService) SetupCache() error {
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

func RandomNetwork(twoGProb, threeGProb, fourGProb float64) string {
	randomNumber := rand.Float64()
	switch {
	case randomNumber < twoGProb:
		return "2G"
	case randomNumber < twoGProb+threeGProb:
		return "3G"
	case randomNumber < twoGProb+threeGProb+fourGProb:
		return "4G"
	default:
		return "5G"
	}
}

func RandomService(voice, sms, data float64) string {
	randomNumber := rand.Float64()
	switch {
	case randomNumber < voice:
		return "Voice"
	case randomNumber < voice+sms:
		return "SMS"
	case randomNumber < voice+sms+data:
		return "Data"
	default:
		return "Other"
	}
}

func generateCDRID() int32 {
	rand.Seed(time.Now().UnixNano())
	currentTime := time.Now().Unix()
	lastSixDigits := currentTime % 1000000
	randomTwoDigits := rand.Intn(90) + 10
	combined := fmt.Sprintf("%02d%06d", randomTwoDigits, lastSixDigits)
	combinedInt64, _ := strconv.ParseInt(combined, 10, 32)
	return int32(combinedInt64)
}

func getNextCdrID() int {
	rand.Seed(time.Now().UnixNano())
	return int(atomic.AddInt32(&cdrId, 1))
}

func getStartAndEndInterval(t time.Time) (time.Time, time.Time) {
	totalMinutes := t.Hour()*60 + t.Minute()
	intervalMinutes := totalMinutes / 30 * 30
	start := time.Date(t.Year(), t.Month(), t.Day(), intervalMinutes/60, intervalMinutes%60, 0, 0, t.Location())
	return start, start.Add(30 * time.Minute)
}

func getRandomDate(start, end time.Time) time.Time {
	duration := end.Sub(start).Seconds()
	randomOffset := rand.Int63n(int64(duration))
	return start.Add(time.Duration(randomOffset) * time.Second)
}

func GetCallDurationSec() int {
	randomChoice := rand.Float64()
	switch {
	case randomChoice < 0.80:
		return rand.Intn(600) + 1
	case randomChoice < 0.85:
		return 0
	default:
		return rand.Intn(3000) + 601
	}
}

func GetCallIntervals(callStartTime, callEndTime, intervalStartTime, intervalEndTime time.Time) ([]map[string]interface{}, error) {
	var intervals []map[string]interface{}
	if callEndTime.Before(intervalStartTime) {
		return intervals, nil
	}
	currentStartTime := callStartTime
	currentEndTime := intervalEndTime
	for currentStartTime.Before(callEndTime) {
		if currentStartTime.Before(intervalStartTime) {
			currentStartTime = intervalStartTime
		}
		if currentEndTime.After(callEndTime) {
			currentEndTime = callEndTime
		}
		intervals = append(intervals, map[string]interface{}{
			"start":    currentStartTime.Format("2006-01-02 15:04:05"),
			"end":      currentEndTime.Format("2006-01-02 15:04:05"),
			"duration": int(currentEndTime.Sub(currentStartTime).Seconds()),
		})
		if currentEndTime.Equal(callEndTime) {
			break
		}
		currentStartTime = currentEndTime
		currentEndTime = currentEndTime.Add(30 * time.Minute)
	}
	return intervals, nil
}

func (c *CdrGeneratorService) GetCustomers() (entities.Customer, entities.Customer, string, error) {

	rand.Seed(time.Now().UnixNano())

	// Probabilities
	probHome := 0.60
	probNational := 0.39
	//	probInternational := 1 - probHome - probNational

	// Generate a random number for the CallerType
	CallerTypeValue := rand.Float64()
	var CallerType string
	var roamingIndicator bool

	// Determine CallerType and roaming indicator
	switch {
	case CallerTypeValue < probHome:
		CallerType = "Home"
	case CallerTypeValue < probHome+probNational:
		CallerType = "National"
		roamingIndicator = true
	default:
		CallerType = "International"
		roamingIndicator = true
	}

	// Generate a random number for the CalledType
	CalledTypeValue := rand.Float64()
	var CalledType string

	// Determine CalledType
	switch {
	case CalledTypeValue < probHome:
		CalledType = "Home"
	case CalledTypeValue < probHome+probNational:
		CalledType = "National"
	default:
		CalledType = "International"
	}

	// Fetch random customer by type from the repository
	var callerCustomer, calledCustomer *entities.Customer
	var err error

	// Get random caller customer (pointer)
	callerCustomer, err = c.CustomerInmemRepo.GetRandomByCustomerType(CallerType)
	if err != nil {
		return entities.Customer{}, entities.Customer{}, "", err
	}

	// Make sure the called customer is different from the caller
	for {
		calledCustomer, err = c.CustomerInmemRepo.GetRandomByCustomerType(CalledType)
		if err != nil {
			return entities.Customer{}, entities.Customer{}, "", err
		}

		if calledCustomer.ID != callerCustomer.ID {
			break
		}
	}

	// Convert roamingIndicator to string
	roamingStr := "No"
	if roamingIndicator {
		roamingStr = "Yes"
	}

	// Dereference the pointer if needed
	return *callerCustomer, *calledCustomer, roamingStr, nil
}

func (c *CdrGeneratorService) Generate() error {
	cdrId = generateCDRID()
	if err := c.SetupCache(); err != nil {
		return fmt.Errorf("failed to set up cache: %v", err)
	}
	var cdrFuture []entities.Cdr

	startTimeInterval, endTimeInterval := getStartAndEndInterval(time.Now())
	for i := 0; i < 2; i++ {
		for j := 0; j < 10; j++ {
			networkTechnology := RandomNetwork(0.05, 0.4, 0.55)
			serviceCategory := RandomService(0.4, 0.1, 0.45)
			serviceType, err := c.ServiceTypeInmemRepo.GetByNetworkTechnologyAndName(networkTechnology, serviceCategory)
			if err != nil {
				fmt.Println("Error:", err)
				continue
			}
			networkElement, err := c.NetworkElementInmemRepo.GetRandomRanByNetworkTechnology(networkTechnology)
			if err != nil {
				fmt.Println("Error:", err)
				continue
			}
			var tac string
			if networkElement.TAC != nil {
				tac = *networkElement.TAC
			} else {
				tac = ""
			}
			var lac string
			if networkElement.LAC != nil {
				lac = *networkElement.LAC
			} else {
				lac = ""
			}
			caller, called, roamingIndicator, err := c.GetCustomers()

			if err != nil {
				log.Fatalf("Error generating customers: %v", err)
			}

			cdr := &entities.Cdr{
				ServiceType:        serviceType.Name,
				CallingPartyNumber: caller.MSISDN,
				CalledPartyNumber:  called.MSISDN,
				TerminationCause:   "Normal Release",
				RoamingIndicator:   roamingIndicator,
				IMSI:               caller.IMSI,
				IMEI:               caller.IMEI,
				TAC:                tac,
				LAC:                lac,
				CellID:             *networkElement.CellID,
			}
			eventStartTime := getRandomDate(startTimeInterval, endTimeInterval)
			if serviceCategory == "SMS" {
				eventEndTime := eventStartTime.Add(5 * time.Second)
				cdr.MessageLength = rand.Intn(2048) + 1
				cdr.DeliveryStatus = "Delivered"
				cdr.Reference = fmt.Sprintf("SMS-%d", cdrId)
				cdr.StartTime = eventStartTime.Format("2006-01-02 15:04:05")
				cdr.EndTime = eventEndTime.Format("2006-01-02 15:04:05")
				cdrId := getNextCdrID()
				cdr.ID = cdrId
				c.CdrInmemRepo.Insert(*cdr)
			} else if serviceCategory == "Voice" {
				callDurationSec := GetCallDurationSec()
				eventEndTime := eventStartTime.Add(time.Duration(callDurationSec) * time.Second)
				intervals, err := GetCallIntervals(eventStartTime, eventEndTime, startTimeInterval, endTimeInterval)
				if err != nil {
					return fmt.Errorf("error in calculating call intervals: %v", err)
				}
				cdr.Reference = fmt.Sprintf("CAL-%d", cdrId)
				if len(intervals) == 1 {
					cdr.StartTime = eventStartTime.Format("2006-01-02 15:04:05")
					cdr.EndTime = eventEndTime.Format("2006-01-02 15:04:05")
					cdr.Duration = callDurationSec
					cdrId := getNextCdrID()
					cdr.ID = cdrId
					c.CdrInmemRepo.Insert(*cdr)
				} else {
					for k, interval := range intervals {
						cdr.StartTime = interval["start"].(string)
						cdr.EndTime = interval["end"].(string)
						cdr.Duration = interval["duration"].(int)
						if k == 0 {
							cdrId := getNextCdrID()
							cdr.ID = cdrId
							c.CdrInmemRepo.Insert(*cdr)
						} else {
							cdr.ID = 0
							cdrFuture = append(cdrFuture, *cdr)
						}
					}
				}
			} else if serviceCategory == "Data" {
				callDurationSec := GetCallDurationSec()
				eventEndTime := eventStartTime.Add(time.Duration(callDurationSec) * time.Second)
				intervals, err := GetCallIntervals(eventStartTime, eventEndTime, startTimeInterval, endTimeInterval)
				if err != nil {
					return fmt.Errorf("error in calculating call intervals: %v", err)
				}
				cdr.Reference = fmt.Sprintf("SES-%d", cdrId)
				if len(intervals) == 1 {
					cdr.StartTime = eventStartTime.Format("2006-01-02 15:04:05")
					cdr.EndTime = eventEndTime.Format("2006-01-02 15:04:05")
					cdr.Duration = callDurationSec
					cdrId := getNextCdrID()
					cdr.ID = cdrId
					c.CdrInmemRepo.Insert(*cdr)
				} else {
					for k, interval := range intervals {
						cdr.StartTime = interval["start"].(string)
						cdr.EndTime = interval["end"].(string)
						cdr.Duration = interval["duration"].(int)
						if k == 0 {
							cdrId := getNextCdrID()
							cdr.ID = cdrId
							c.CdrInmemRepo.Insert(*cdr)
						} else {
							cdr.ID = 0
							cdrFuture = append(cdrFuture, *cdr)
						}
					}
				}
			} else {
				cdr.Reference = fmt.Sprintf("OTH-%d", cdrId)
				cdrId := getNextCdrID()
				cdr.ID = cdrId
				c.CdrInmemRepo.Insert(*cdr)
			}
		}
	}

	count, err := c.CdrInmemRepo.Length()
	if err != nil {
		log.Fatalf("Error getting CDR count: %v", err)
	}
	fmt.Printf("Total CDRs: %d - Total Future CDRs %d\n", count, len(cdrFuture))

	// Retrieve all CDRs from the repository
	cdrs, err := c.CdrInmemRepo.GetAll()
	if err != nil {
		log.Fatalf("Error retrieving CDRs: %v", err)
	}

	// Print all CDRs
	for _, cdr := range cdrs {
		fmt.Printf("CDR ID: %d, ServiceType: %s, NetworkTechnology: %s, StartTime: %s, EndTime: %s, Duration: %d seconds\n",
			cdr.ID, cdr.ServiceType, cdr.NetworkTechnology, cdr.StartTime, cdr.EndTime, cdr.Duration)
	}
	fmt.Printf("--\n")
	for _, cdr := range cdrFuture {
		fmt.Printf("CDR ID: %d, ServiceType: %s, NetworkTechnology: %s, StartTime: %s, EndTime: %s, Duration: %d seconds\n",
			cdr.ID, cdr.ServiceType, cdr.NetworkTechnology, cdr.StartTime, cdr.EndTime, cdr.Duration)
	}
	return nil
}
