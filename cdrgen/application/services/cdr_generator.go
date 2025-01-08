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

func RandomService(voice, sms, data float64) string {
	randomNumber := rand.Float64()

	if randomNumber < voice {
		return "Voice"
	} else if randomNumber < voice+sms {
		return "SMS"
	} else if randomNumber < voice+sms+data {
		return "Data"
	} else {
		return "Other"
	}
}

func generateCDRID() int32 {
	// Seed the random number generator
	rand.Seed(time.Now().UnixNano())

	// Get the current Unix timestamp
	currentTime := time.Now().Unix()

	// Extract the last 6 digits of the timestamp
	lastSixDigits := currentTime % 1000000

	// Generate a random two-digit number
	randomTwoDigits := rand.Intn(90) + 10

	// Combine the two-digit number and the last six digits
	combined := fmt.Sprintf("%02d%06d", randomTwoDigits, lastSixDigits)

	// Convert the combined string to an int32
	combinedInt64, err := strconv.ParseInt(combined, 10, 32)
	if err != nil {
		// Handle the error if conversion fails
		fmt.Printf("Error converting combined to int32: %v\n", err)
		return 0 // Return 0 or an error-specific value
	}

	// Return the combined value as int32
	return int32(combinedInt64)
}

func getNextCdrID() int {
	// Increment cdrId atomically and return the new value
	newCdrID := atomic.AddInt32(&cdrId, 1)

	// Return the incremented CDR ID as an int
	return int(newCdrID)
}

func (c *CdrGeneratorService) Generate() error {
	cdrId = generateCDRID()
	// Setup the cache
	if err := c.SetupCache(); err != nil {
		return fmt.Errorf("failed to set up cache: %v", err)
	}

	// Generate 10 CDRs
	for i := 0; i < 10; i++ {

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

		cdrId := getNextCdrID()
		cdr := &entities.Cdr{
			ID:                cdrId,
			ServiceType:       serviceType.Name,
			NetworkTechnology: networkTechnology,
			TAC:               tac,
			LAC:               lac,
			CellID:            *networkElement.CellID,
		}

		// Log the generated CDR
		log.Printf("Generated CDR #%d: %+v", i+1, cdr)
	}
	return nil
}
