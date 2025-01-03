package services

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
)

// LoaderService manages database operations and data loading.
type LoaderService struct {
	DB                     *sql.DB
	NetworkTechRepo        *sqlitestore.NetworkTechnologyRepository
	NetworkElementTypeRepo *sqlitestore.NetworkElementTypeRepository
	ServiceTypeRepo        *sqlitestore.ServiceTypeRepository
}

// NewLoaderService initializes the LoaderService with all repositories.
func NewLoaderService(dbFile string) (*LoaderService, error) {
	// Open database connection
	db, err := sql.Open("sqlite3", dbFile)
	if err != nil {
		return nil, fmt.Errorf("could not open database: %v", err)
	}

	// Ping to verify the connection
	if err := db.Ping(); err != nil {
		db.Close()
		return nil, fmt.Errorf("could not connect to database: %v", err)
	}

	// Initialize repositories
	networkTechRepo := sqlitestore.NewNetworkTechnologyRepository(db)
	networkElemRepo := sqlitestore.NewNetworkElementTypeRepository(db)
	serviceTypeRepo := sqlitestore.NewServiceTypeRepository(db)

	return &LoaderService{
		DB:                     db,
		NetworkTechRepo:        networkTechRepo,
		NetworkElementTypeRepo: networkElemRepo,
		ServiceTypeRepo:        serviceTypeRepo,
	}, nil
}

// SetupDatabase creates all necessary tables for the application.
func (l *LoaderService) SetupDatabase() error {
	if err := l.NetworkTechRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create network technology table: %v", err)
	}
	if err := l.NetworkElementTypeRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create network element type table: %v", err)
	}
	if err := l.ServiceTypeRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create service type table: %v", err)
	}
	log.Println("All tables created successfully.")
	return nil
}

// LoadAndSaveData loads data from a JSON file, creates tables if not present, and saves the data to the database.
func (l *LoaderService) LoadAndSaveBaseline(filename string) error {
	// Ensure the database tables are created
	if err := l.SetupDatabase(); err != nil {
		return fmt.Errorf("failed to set up database tables: %v", err)
	}

	// Read the file content
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return fmt.Errorf("could not read file: %v", err)
	}

	// Unmarshal JSON data
	var jsonData struct {
		NetworkTechnologies []entities.NetworkTechnology  `json:"network_technologies"`
		NetworkElements     []entities.NetworkElementType `json:"network_element_types"`
		ServiceTypes        []entities.ServiceType        `json:"service_types"`
	}
	if err := json.Unmarshal(data, &jsonData); err != nil {
		return fmt.Errorf("could not unmarshal json: %v", err)
	}

	// Save network technologies to the database
	for _, nt := range jsonData.NetworkTechnologies {
		if err := l.NetworkTechRepo.Insert(nt); err != nil {
			return fmt.Errorf("error saving network technology: %v", err)
		}
	}

	// Save network elements to the database
	for _, ne := range jsonData.NetworkElements {
		if err := l.NetworkElementTypeRepo.Insert(ne); err != nil {
			return fmt.Errorf("error saving network element: %v", err)
		}
	}

	// Save service types to the database
	for _, st := range jsonData.ServiceTypes {
		if err := l.ServiceTypeRepo.Insert(st); err != nil {
			return fmt.Errorf("error saving service type: %v", err)
		}
	}

	log.Println("Data loaded and saved successfully.")
	return nil
}

// Close closes the database connection.
func (l *LoaderService) Close() error {
	if l.DB != nil {
		err := l.DB.Close()
		if err != nil {
			return fmt.Errorf("error closing database: %v", err)
		}
		log.Println("Database connection closed successfully.")
	}
	return nil
}
