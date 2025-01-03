package services

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"

	"gopkg.in/yaml.v3"

	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/domain/factories"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
)

type LoaderService struct {
	DB                     *sql.DB
	NetworkTechRepo        *sqlitestore.NetworkTechnologyRepository
	NetworkElementTypeRepo *sqlitestore.NetworkElementTypeRepository
	ServiceTypeRepo        *sqlitestore.ServiceTypeRepository
	LocationRepo           *sqlitestore.LocationRepository
}

// NewLoaderService initializes the LoaderService with all repositories.
func NewLoaderService(dbFile string) (*LoaderService, error) {
	db, err := sql.Open("sqlite3", dbFile)
	if err != nil {
		return nil, fmt.Errorf("could not open database: %v", err)
	}

	if err := db.Ping(); err != nil {
		db.Close()
		return nil, fmt.Errorf("could not connect to database: %v", err)
	}

	return &LoaderService{
		DB:                     db,
		NetworkTechRepo:        sqlitestore.NewNetworkTechnologyRepository(db),
		NetworkElementTypeRepo: sqlitestore.NewNetworkElementTypeRepository(db),
		ServiceTypeRepo:        sqlitestore.NewServiceTypeRepository(db),
		LocationRepo:           sqlitestore.NewLocationRepository(db),
	}, nil
}

// SetupDatabase creates all necessary tables.
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
	if err := l.LocationRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create location table: %v", err)
	}
	log.Println("All tables created successfully.")
	return nil
}

// LoadAndSaveBaseline reads data from a JSON file, creates baseline tables, and saves the data.
func (l *LoaderService) LoadAndSaveBaseline(jsonFilename string) error {
	if err := l.SetupDatabase(); err != nil {
		return fmt.Errorf("failed to set up database tables: %v", err)
	}

	data, err := ioutil.ReadFile(jsonFilename)
	if err != nil {
		return fmt.Errorf("could not read JSON file: %v", err)
	}

	var jsonData struct {
		NetworkTechnologies []entities.NetworkTechnology  `json:"network_technologies"`
		NetworkElements     []entities.NetworkElementType `json:"network_element_types"`
		ServiceTypes        []entities.ServiceType        `json:"service_types"`
	}
	if err := json.Unmarshal(data, &jsonData); err != nil {
		return fmt.Errorf("could not unmarshal JSON: %v", err)
	}

	for _, nt := range jsonData.NetworkTechnologies {
		if err := l.NetworkTechRepo.Insert(nt); err != nil {
			return fmt.Errorf("error saving network technology: %v", err)
		}
	}
	for _, ne := range jsonData.NetworkElements {
		if err := l.NetworkElementTypeRepo.Insert(ne); err != nil {
			return fmt.Errorf("error saving network element: %v", err)
		}
	}
	for _, st := range jsonData.ServiceTypes {
		if err := l.ServiceTypeRepo.Insert(st); err != nil {
			return fmt.Errorf("error saving service type: %v", err)
		}
	}

	log.Println("Baseline data loaded and saved successfully.")
	return nil
}

// LoadAndSaveBusiness reads location data from a YAML file and saves it to the database.
func (l *LoaderService) LoadAndSaveBusiness(yamlFilename string) error {
	data, err := ioutil.ReadFile(yamlFilename)
	if err != nil {
		return fmt.Errorf("could not read YAML file: %v", err)
	}

	// Unmarshal YAML data into the mappers.Config struct
	var config mappers.Config
	if err := yaml.Unmarshal(data, &config); err != nil {
		return fmt.Errorf("could not unmarshal YAML: %v", err)
	}

	// Generate locations based on the configuration
	locations, err := factories.GenerateLocations(&config)
	if err != nil {
		return fmt.Errorf("error generating locations: %v", err)
	}

	// Insert the generated locations into the database
	for _, lc := range locations {
		if err := l.LocationRepo.Insert(*lc); err != nil { // Dereference lc here
			return fmt.Errorf("error saving location: %v", err)
		}
	}
	log.Println("Business data (locations) loaded and saved successfully.")
	return nil
}

// Close closes the database connection.
func (l *LoaderService) Close() error {
	if l.DB != nil {
		err := l.DB.Close()
		if err != nil {
			return err
		}
		log.Println("Database connection closed successfully.")
	}
	return nil
}
