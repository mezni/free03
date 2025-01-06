package services

import (
	"database/sql"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
	"log"
	"math/rand"
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

// NewLoaderService initializes the LoaderService with all repositories.
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
	// Step 1: Fetch all network technologies from the SQLite repository
	networkTechnologies, err := c.NetworkTechSqliteRepo.GetAll()
	if err != nil {
		return fmt.Errorf("failed to fetch network technologies from SQLite repository: %v", err)
	}

	// Step 2: Write all network technologies to the in-memory repository
	for _, tech := range networkTechnologies {
		err := c.NetworkTechInmemRepo.Insert(tech)
		if err != nil {
			log.Printf("warning: failed to insert network technology with ID %d into in-memory repository: %v", tech.ID, err)
		}
	}

	log.Printf("successfully cached %d network technologies", len(networkTechnologies))

	networkElements, err := c.NetworkElementSqliteRepo.GetAll()
	if err != nil {
		return fmt.Errorf("failed to fetch network elements from SQLite repository: %v", err)
	}

	// Step 2: Write all network technologies to the in-memory repository
	for _, ne := range networkElements {
		err := c.NetworkElementInmemRepo.Insert(ne)
		if err != nil {
			log.Printf("warning: failed to insert network element with ID %d into in-memory repository: %v", ne.ID, err)
		}
	}

	log.Printf("successfully cached %d network elements", len(networkElements))

	serviceTypes, err := c.ServiceTypeSqliteRepo.GetAll()
	if err != nil {
		return fmt.Errorf("failed to fetch service types from SQLite repository: %v", err)
	}

	// Step 2: Write all network technologies to the in-memory repository
	for _, st := range serviceTypes {
		err := c.ServiceTypeInmemRepo.Insert(st)
		if err != nil {
			log.Printf("warning: failed to insert service types with ID %d into in-memory repository: %v", st.ID, err)
		}
	}

	log.Printf("successfully cached %d service types", len(serviceTypes))

	customers, err := c.CustomerSqliteRepo.GetAll()
	if err != nil {
		return fmt.Errorf("failed to fetch customers from SQLite repository: %v", err)
	}

	// Step 2: Write all network technologies to the in-memory repository
	for _, cs := range customers {
		err := c.CustomerInmemRepo.Insert(cs)
		if err != nil {
			log.Printf("warning: failed to insert customers with ID %d into in-memory repository: %v", cs.ID, err)
		}
	}

	log.Printf("successfully cached %d customers", len(customers))

	return nil
}

func RandomNetwork(twoGProb, threeGProb, fourGProb float64) string {
	rand.Seed(time.Now().UnixNano())
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

func (c *CdrGeneratorService) GetCustomers(callingCustomerType, calledCustomerType string) (entities.Customer, entities.Customer, error) {
	// Fetch a random customer for the calling party
	callingCustomerPtr, err := c.CustomerInmemRepo.GetRandomByCustomerType(callingCustomerType)
	if err != nil {
		return entities.Customer{}, entities.Customer{}, fmt.Errorf("failed to fetch calling customer: %v", err)
	}
	// Dereference the pointer to get the value
	callingCustomer := *callingCustomerPtr

	var calledCustomer entities.Customer

	// Fetch a random customer for the called party, ensuring it's different from the calling customer
	for {
		calledCustomerPtr, err := c.CustomerInmemRepo.GetRandomByCustomerType(calledCustomerType)
		if err != nil {
			return entities.Customer{}, entities.Customer{}, fmt.Errorf("failed to fetch called customer: %v", err)
		}
		// Dereference the pointer to get the value
		calledCustomer = *calledCustomerPtr

		// Ensure the called customer is not the same as the calling customer
		if calledCustomer.ID != callingCustomer.ID {
			break
		}
	}

	return callingCustomer, calledCustomer, nil
}

func GetRandomCustomerType(customerTypes []string, customerProbabilities []float64) (string, error) {
	// Validate inputs
	if len(customerTypes) != len(customerProbabilities) {
		return "", fmt.Errorf("customerTypes and customerProbabilities must have the same length")
	}

	// Calculate cumulative probabilities
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

	// Generate a random number between 0 and 1
	rand.Seed(time.Now().UnixNano())
	randomNumber := rand.Float64()

	// Select the customer type based on the random number
	for i, cumProb := range cumulativeProbabilities {
		if randomNumber <= cumProb {
			return customerTypes[i], nil
		}
	}

	return "", fmt.Errorf("failed to select customer type")
}

func (c *CdrGeneratorService) Generate() error {
	// Setup the cache
	if err := c.SetupCache(); err != nil {
		return fmt.Errorf("failed to set up cache: %v", err)
	}

	// Randomly select a network technology
	networkTechnology := RandomNetwork(0.05, 0.4, 0.55)
	log.Printf("Selected Network Technology: %s", networkTechnology)

	customerTypes := []string{"Home", "National", "International"}
	callerProbabilities := []float64{0.75, 0.2, 0.05}
	calleeProbabilities := []float64{0.55, 0.4, 0.05}
	callerType, err := GetRandomCustomerType(customerTypes, callerProbabilities)
	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	calleeType, err := GetRandomCustomerType(customerTypes, calleeProbabilities)
	if err != nil {
		log.Fatalf("Error: %v", err)
	}
	log.Printf("%s %s", callerType, calleeType)

	// Get two different customers
	callingCustomer, calledCustomer, err := c.GetCustomers(callerType, calleeType)
	if err != nil {
		return fmt.Errorf("failed to get two different customers: %v", err)
	}

	log.Printf("Calling Customer: %+v", callingCustomer)
	log.Printf("Called Customer: %+v", calledCustomer)
	return nil
}
