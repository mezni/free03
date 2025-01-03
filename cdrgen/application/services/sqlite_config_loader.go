package services

import (
	"database/sql"
	"log"

	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
)

type LoaderService struct {
	DB                   *sql.DB
	NetworkTechRepo      *sqlitestore.NetworkTechnologyRepository
	NetworkElementTypeRepo *sqlitestore.NetworkElementTypeRepository
	ServiceTypeRepo      *sqlitestore.ServiceTypeRepository
}

// NewLoaderService initializes the LoaderService with all repositories.
func NewLoaderService(dbFile string) (*LoaderService, error) {
	// Open database connection
	db, err := sql.Open("sqlite3", dbFile)
	if err != nil {
		return nil, err
	}

	// Ping to verify the connection
	if err := db.Ping(); err != nil {
		db.Close()
		return nil, err
	}

	// Initialize repositories
	networkTechRepo := sqlitestore.NewNetworkTechnologyRepository(db)
	networkElemRepo := sqlitestore.NewNetworkElementTypeRepository(db)
	serviceTypeRepo := sqlitestore.NewServiceTypeRepository(db)

	// Return the LoaderService
	return &LoaderService{
		DB:                   db,
		NetworkTechRepo:      networkTechRepo,
		NetworkElementTypeRepo: networkElemRepo,
		ServiceTypeRepo:      serviceTypeRepo,
	}, nil
}

// SetupDatabase creates all necessary tables for the application.
func (l *LoaderService) SetupDatabase() error {
	if err := l.NetworkTechRepo.CreateTable(); err != nil {
		return err
	}
	if err := l.NetworkElementTypeRepo.CreateTable(); err != nil {
		return err
	}
	if err := l.ServiceTypeRepo.CreateTable(); err != nil {
		return err
	}
	log.Println("All tables created successfully.")
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
