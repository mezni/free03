package services

import (
	"database/sql"
	"fmt"
	"log"


//	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
	"github.com/mezni/wovoka/cdrgen/infrastructure/inmemstore"
)

type CdrGeneratorService struct {
	DB                     *sql.DB
	NetworkTechSqliteRepo        *sqlitestore.NetworkTechnologyRepository
	NetworkElementTypeSqliteRepo *sqlitestore.NetworkElementTypeRepository
	ServiceTypeSqliteRepo        *sqlitestore.ServiceTypeRepository
	ServiceNodeSqliteRepo        *sqlitestore.ServiceNodeRepository
	LocationSqliteRepo           *sqlitestore.LocationRepository
	NetworkElementSqliteRepo     *sqlitestore.NetworkElementRepository
	CustomerSqliteRepo           *sqlitestore.CustomerRepository
	NetworkTechInmemRepo        *inmemstore.InMemNetworkTechnologyRepository
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
		DB:                     db,
		NetworkTechSqliteRepo:        sqlitestore.NewNetworkTechnologyRepository(db),
		NetworkElementTypeSqliteRepo: sqlitestore.NewNetworkElementTypeRepository(db),
		ServiceTypeSqliteRepo:        sqlitestore.NewServiceTypeRepository(db),
		ServiceNodeSqliteRepo:        sqlitestore.NewServiceNodeRepository(db),
		LocationSqliteRepo:           sqlitestore.NewLocationRepository(db),
		NetworkElementSqliteRepo:     sqlitestore.NewNetworkElementRepository(db),
		CustomerSqliteRepo:           sqlitestore.NewCustomerRepository(db),
		NetworkTechInmemRepo:         inmemstore.NewInMemNetworkTechnologyRepository(),
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
	return nil
}


func (c *CdrGeneratorService) Generate() error {
	// Setup the cache
	if err := c.SetupCache(); err != nil {
		return fmt.Errorf("failed to set up cache: %v", err)
	}

	// Additional logic for generation can follow here
	return nil
}