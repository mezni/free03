package sqlitestore

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// NetworkElementRepository handles database operations for network elements.
type NetworkElementRepository struct {
	db *sql.DB
}

// NewNetworkElementRepository creates a new instance of NetworkElementRepository.
func NewNetworkElementRepository(db *sql.DB) *NetworkElementRepository {
	return &NetworkElementRepository{db: db}
}

// CreateTable creates the network_elements table.
func (r *NetworkElementRepository) CreateTable() error {
	_, err := r.db.Exec(CreateNetworkElementsTable)
	if err != nil {
		return fmt.Errorf("failed to create network_elements table: %w", err)
	}
	return nil
}

// Insert inserts a new network element into the database, avoiding duplicates based on name.
func (r *NetworkElementRepository) Insert(networkElement entities.NetworkElement) error {
	var existingID int
	err := r.db.QueryRow(SelectNetworkElementByName, networkElement.Name).Scan(&existingID)
	if err == nil {
		log.Printf("Network element with name %s already exists, skipping insert.\n", networkElement.Name)
		return nil
	}

	if err != sql.ErrNoRows {
		return fmt.Errorf("failed to check for existing network element: %w", err)
	}

	_, err = r.db.Exec(
		InsertNetworkElement,
		networkElement.Name,
		networkElement.Description,
		networkElement.ElementType,
		networkElement.NetworkTechnology,
		networkElement.IPAddress,
		networkElement.Status,
		networkElement.TAC,
		networkElement.LAC,
		networkElement.CellID,
	)
	if err != nil {
		return fmt.Errorf("failed to insert network element: %w", err)
	}

	return nil
}

// GetAll retrieves all network elements from the database.
func (r *NetworkElementRepository) GetAll() ([]entities.NetworkElement, error) {
	rows, err := r.db.Query(SelectAllNetworkElements)
	if err != nil {
		return nil, fmt.Errorf("failed to query network_elements: %w", err)
	}
	defer rows.Close()

	var elements []entities.NetworkElement
	for rows.Next() {
		var elem entities.NetworkElement
		if err := rows.Scan(
			&elem.ID,
			&elem.Name,
			&elem.Description,
			&elem.ElementType,
			&elem.NetworkTechnology,
			&elem.IPAddress,
			&elem.Status,
			&elem.TAC,
			&elem.LAC,
			&elem.CellID,
		); err != nil {
			return nil, fmt.Errorf("failed to scan row into network element: %w", err)
		}
		elements = append(elements, elem)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error occurred during row iteration: %w", err)
	}

	return elements, nil
}
