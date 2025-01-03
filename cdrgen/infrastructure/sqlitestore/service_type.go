package sqlitestore

import (
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

// Insert inserts a new service type into the database.
func (r *ServiceTypeRepository) Insert(serviceType entities.ServiceType) error {
	query := `
		INSERT INTO service_types (Name, Description, NetworkTechnology) 
		VALUES (?, ?, ?)`
	_, err := r.db.Exec(query, serviceType.Name, serviceType.Description, serviceType.NetworkTechnology)
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
