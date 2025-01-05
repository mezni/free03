package services

import (
	"database/sql"
	"fmt"
	"log"
	"time"

//	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/domain/factories"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
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

func (c *CdrGeneratorService) Generate() ( error) {
	// Setup the cache
	if err := c.SetupCache(); err != nil {
		return  fmt.Errorf("failed to set up cache: %v", err)
	}

	// Get service types from the in-memory repository
	serviceTypes, err := c.ServiceTypeInmemRepo.GetAll()
	if err != nil {
		return  fmt.Errorf("failed to fetch service types: %v", err)
	}

	// Prepare configuration for CDR generation
	config := map[string]interface{}{
		"serviceTypes": serviceTypes,
		"startTime":    time.Now(),
	}

	// Generate CDRs
	cdrs, err := factories.GenerateCdr(config)
	if err != nil {
		return  fmt.Errorf("error generating CDRs: %v", err)
	}
	fmt.Println(cdrs)

	return nil
}
