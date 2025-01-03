package sqlitestore

import (
		"log"
	"database/sql"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// ServiceTypeRepository handles database operations for service types.
type ServiceTypeRepository struct {
	db *sql.DB
}

// NewServiceTypeRepository creates a new instance of ServiceTypeRepository.
func NewServiceTypeRepository(db *sql.DB) *ServiceTypeRepository {
	return &ServiceTypeRepository{db: db}
}

// CreateTable creates the service_types table.
func (r *ServiceTypeRepository) CreateTable() error {
	query := `
		CREATE TABLE IF NOT EXISTS service_types (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			Name TEXT NOT NULL,
			Description TEXT NOT NULL,
			NetworkTechnology TEXT NOT NULL
		)`
	_, err := r.db.Exec(query)
	return err
}

// Insert inserts a new service type into the database, but does not insert if a duplicate exists.
func (r *ServiceTypeRepository) Insert(serviceType entities.ServiceType) error {
	// First, check if the service type with the same name and network technology already exists.
	var existingID int
	query := `SELECT id FROM service_types WHERE Name = ? AND NetworkTechnology = ?`
	err := r.db.QueryRow(query, serviceType.Name, serviceType.NetworkTechnology).Scan(&existingID)
	if err == nil {
		// If no error, it means a record with the same name and network technology already exists. Skip the insert.
		// No error is returned, just log the action if needed
		log.Printf("Service type with name %s and network technology %s already exists, skipping insert.\n", serviceType.Name, serviceType.NetworkTechnology)
		return nil // Simply return nil without inserting or throwing an error
	}

	// If the error is not nil (which is expected when no row is found), proceed to insert.
	if err != sql.ErrNoRows {
		// Return any other unexpected error
		return err
	}

	// Insert the new service type if it doesn't already exist.
	insertQuery := `
		INSERT INTO service_types (Name, Description, NetworkTechnology) 
		VALUES (?, ?, ?)`
	_, err = r.db.Exec(insertQuery, serviceType.Name, serviceType.Description, serviceType.NetworkTechnology)
	return err
}



// GetAll retrieves all service types from the database.
func (r *ServiceTypeRepository) GetAll() ([]entities.ServiceType, error) {
	rows, err := r.db.Query(`
		SELECT id, Name, Description, NetworkTechnology FROM service_types`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var services []entities.ServiceType
	for rows.Next() {
		var service entities.ServiceType
		if err := rows.Scan(&service.ID, &service.Name, &service.Description, &service.NetworkTechnology); err != nil {
			return nil, err
		}
		services = append(services, service)
	}
	return services, nil
}
