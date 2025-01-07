package sqlitestore

import (
	"database/sql"
	"fmt"
	"log"

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

// CreateTable creates the service_types table with lowercase column names.
func (r *ServiceTypeRepository) CreateTable() error {
	_, err := r.db.Exec(CreateServiceTypesTable)
	if err != nil {
		return fmt.Errorf("failed to create service_types table: %w", err)
	}
	return nil
}

// Insert inserts a new service type into the database, but does not insert if it already exists.
func (r *ServiceTypeRepository) Insert(serviceType entities.ServiceType) error {
	var existingID int
	err := r.db.QueryRow(SelectServiceTypesByNameAndTech, serviceType.Name, serviceType.NetworkTechnology).Scan(&existingID)
	if err == nil {
		log.Printf("Service type with name %s and network technology %s already exists, skipping insert.\n", serviceType.Name, serviceType.NetworkTechnology)
		return nil
	}

	if err != sql.ErrNoRows {
		return fmt.Errorf("failed to check for existing service type: %w", err)
	}

	_, err = r.db.Exec(InsertServiceType, serviceType.Name, serviceType.Description, serviceType.NetworkTechnology,
		serviceType.BearerType, serviceType.JitterMin, serviceType.JitterMax, serviceType.LatencyMin,
		serviceType.LatencyMax, serviceType.ThroughputMin, serviceType.ThroughputMax, serviceType.PacketLossMin,
		serviceType.PacketLossMax, serviceType.CallSetupTimeMin, serviceType.CallSetupTimeMax, serviceType.MosMin,
		serviceType.MosMax)
	if err != nil {
		return fmt.Errorf("failed to insert service type: %w", err)
	}

	return nil
}

// GetAll retrieves all service types from the database.
func (r *ServiceTypeRepository) GetAll() ([]entities.ServiceType, error) {
	rows, err := r.db.Query(SelectAllServiceTypes)
	if err != nil {
		return nil, fmt.Errorf("failed to query service_types: %w", err)
	}
	defer rows.Close()

	var serviceTypes []entities.ServiceType
	for rows.Next() {
		var serviceType entities.ServiceType
		if err := rows.Scan(&serviceType.ID, &serviceType.Name, &serviceType.Description, &serviceType.NetworkTechnology,
			&serviceType.BearerType, &serviceType.JitterMin, &serviceType.JitterMax, &serviceType.LatencyMin,
			&serviceType.LatencyMax, &serviceType.ThroughputMin, &serviceType.ThroughputMax, &serviceType.PacketLossMin,
			&serviceType.PacketLossMax, &serviceType.CallSetupTimeMin, &serviceType.CallSetupTimeMax, &serviceType.MosMin,
			&serviceType.MosMax); err != nil {
			return nil, fmt.Errorf("failed to scan row into serviceType: %w", err)
		}
		serviceTypes = append(serviceTypes, serviceType)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error occurred during row iteration: %w", err)
	}

	return serviceTypes, nil
}
