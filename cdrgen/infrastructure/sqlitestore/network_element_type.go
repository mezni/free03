package sqlitestore

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// NetworkElementTypeRepository handles database operations for network element types.
type NetworkElementTypeRepository struct {
	db *sql.DB
}

// NewNetworkElementTypeRepository creates a new instance of NetworkElementTypeRepository.
func NewNetworkElementTypeRepository(db *sql.DB) *NetworkElementTypeRepository {
	return &NetworkElementTypeRepository{db: db}
}

// CreateTable creates the network_element_types table with lowercase column names.
func (r *NetworkElementTypeRepository) CreateTable() error {
	_, err := r.db.Exec(CreateNetworkElementTypesTable)
	if err != nil {
		return fmt.Errorf("failed to create network_element_types table: %w", err)
	}
	return nil
}

// Insert inserts a new network element type into the database, but does not insert if it already exists (based on Name and NetworkTechnology).
func (r *NetworkElementTypeRepository) Insert(networkElementType entities.NetworkElementType) error {
	var existingID int
	err := r.db.QueryRow(SelectNetworkElementTypesByNameAndTech, networkElementType.Name, networkElementType.NetworkTechnology).Scan(&existingID)
	if err == nil {
		log.Printf("Network element type with name %s and network technology %s already exists, skipping insert.\n", networkElementType.Name, networkElementType.NetworkTechnology)
		return nil
	}

	if err != sql.ErrNoRows {
		return fmt.Errorf("failed to check for existing network element type: %w", err)
	}

	_, err = r.db.Exec(InsertNetworkElementType, networkElementType.Name, networkElementType.Description, networkElementType.NetworkTechnology)
	if err != nil {
		return fmt.Errorf("failed to insert network element type: %w", err)
	}

	return nil
}

// GetAll retrieves all network element types from the database.
func (r *NetworkElementTypeRepository) GetAll() ([]entities.NetworkElementType, error) {
	rows, err := r.db.Query(SelectAllNetworkElementTypes)
	if err != nil {
		return nil, fmt.Errorf("failed to query network_element_types: %w", err)
	}
	defer rows.Close()

	var elementTypes []entities.NetworkElementType
	for rows.Next() {
		var elemType entities.NetworkElementType
		if err := rows.Scan(&elemType.ID, &elemType.Name, &elemType.Description, &elemType.NetworkTechnology); err != nil {
			return nil, fmt.Errorf("failed to scan row into networkElementType: %w", err)
		}
		elementTypes = append(elementTypes, elemType)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error occurred during row iteration: %w", err)
	}

	return elementTypes, nil
}
