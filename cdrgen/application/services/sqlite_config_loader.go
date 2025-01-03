package services

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/application/interfaces"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
)

type LoaderService struct {
	DB              *sql.DB
	NetworkTechRepo *sqlitestore.NetworkTechnologyRepository
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
		DB:              db,
		NetworkTechRepo: sqlitestore.NewNetworkTechnologyRepository(db),
	}, nil
}

// SetupDatabase creates all necessary tables.
func (l *LoaderService) SetupDatabase() error {
	if err := l.NetworkTechRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create network technology table: %v", err)
	}
	log.Println("All tables created successfully.")
	return nil
}

// LoadNetworkTechnologies processes the NetworkTechnologies and inserts them into the database.
func (l *LoaderService) LoadNetworkTechnologies(networkTechnologies []interfaces.NetworkTechnology) error {
	tx, err := l.DB.Begin()
	if err != nil {
		return fmt.Errorf("could not begin transaction: %v", err)
	}

	// Convert []interfaces.NetworkTechnology to []entities.NetworkTechnology
	var entityNetworkTechnologies []entities.NetworkTechnology
	for _, nt := range networkTechnologies {
		// Map the fields from interfaces.NetworkTechnology to entities.NetworkTechnology
		entity := entities.NetworkTechnology{
			ID:          0,
			Name:        nt.Name,
			Description: nt.Description,
		}
		entityNetworkTechnologies = append(entityNetworkTechnologies, entity)
	}

	// Insert each entity into the database
	for _, entity := range entityNetworkTechnologies {
		if err := l.NetworkTechRepo.Insert(entity); err != nil {
			tx.Rollback()
			return fmt.Errorf("error saving network technology %s: %v", entity.Name, err)
		}
		log.Printf("Successfully inserted network technology: %s", entity.Name)
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("could not commit transaction: %v", err)
	}

	log.Printf("Successfully inserted %d network technologies", len(entityNetworkTechnologies))
	return nil
}

func (l *LoaderService) Load() error {
	// Step 1: Setup the database (create necessary tables)
	if err := l.SetupDatabase(); err != nil {
		return fmt.Errorf("failed to set up database tables: %v", err)
	}

	// Step 2: Read JSON data from the file
	jsonData, err := interfaces.ReadConfig() // Don't redeclare jsonData here
	if err != nil {
		return fmt.Errorf("could not read JSON file: %v", err)
	}

	// Step 3: Load Network Technologies into the database
	log.Printf("Started loading %d network technologies", len(jsonData.NetworkTechnologies))
	if err := l.LoadNetworkTechnologies(jsonData.NetworkTechnologies); err != nil {
		return fmt.Errorf("failed to load network technologies: %v", err)
	}

	return nil
}

// Close closes the database connection.
func (l *LoaderService) Close() error {
	if l.DB != nil {
		err := l.DB.Close()
		if err != nil {
			log.Printf("Error closing database connection: %v", err)
			return err
		}
		log.Println("Database connection closed successfully.")
	}
	return nil
}
