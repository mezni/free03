package sqlitestore

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// ServiceNodeRepository handles database operations for service nodes.
type ServiceNodeRepository struct {
	db *sql.DB
}

// NewServiceNodeRepository creates a new instance of ServiceNodeRepository.
func NewServiceNodeRepository(db *sql.DB) *ServiceNodeRepository {
	return &ServiceNodeRepository{db: db}
}

// CreateTable creates the service_nodes table if it doesn't exist.
func (r *ServiceNodeRepository) CreateTable() error {
	_, err := r.db.Exec(CreateServiceNodesTable)
	if err != nil {
		return fmt.Errorf("failed to create service_nodes table: %w", err)
	}
	return nil
}

// Insert inserts a new service node into the database if it doesn't already exist.
func (r *ServiceNodeRepository) Insert(serviceNode entities.ServiceNode) error {
	var existingID int
	err := r.db.QueryRow(SelectServiceNodesByNameAndTechAndServ, serviceNode.Name, serviceNode.NetworkTechnology, serviceNode.ServiceName).Scan(&existingID)
	if err == nil {
		log.Printf("Service node with name %s, service name %s, and network technology %s already exists, skipping insert.\n", serviceNode.Name, serviceNode.ServiceName, serviceNode.NetworkTechnology)
		return nil
	}

	if err != sql.ErrNoRows {
		return fmt.Errorf("failed to check for existing service node: %w", err)
	}

	_, err = r.db.Exec(InsertServiceNode, serviceNode.Name, serviceNode.ServiceName, serviceNode.NetworkTechnology)
	if err != nil {
		return fmt.Errorf("failed to insert service node: %w", err)
	}

	return nil
}

// GetAll retrieves all service nodes from the database.
func (r *ServiceNodeRepository) GetAll() ([]entities.ServiceNode, error) {
	rows, err := r.db.Query(SelectAllServiceNodes)
	if err != nil {
		return nil, fmt.Errorf("failed to query service_nodes: %w", err)
	}
	defer rows.Close()

	var serviceNodes []entities.ServiceNode
	for rows.Next() {
		var serviceNode entities.ServiceNode
		if err := rows.Scan(&serviceNode.ID, &serviceNode.Name, &serviceNode.ServiceName, &serviceNode.NetworkTechnology); err != nil {
			return nil, fmt.Errorf("failed to scan row into serviceNode: %w", err)
		}
		serviceNodes = append(serviceNodes, serviceNode)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error occurred during row iteration: %w", err)
	}

	return serviceNodes, nil
}
