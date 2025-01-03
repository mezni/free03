package sqlitestore

import (
	"database/sql"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"log"
)

// NetworkTechnologyRepository handles database operations for network technologies.
type NetworkTechnologyRepository struct {
	db *sql.DB
}

// NewNetworkTechnologyRepository creates a new instance of NetworkTechnologyRepository.
func NewNetworkTechnologyRepository(db *sql.DB) *NetworkTechnologyRepository {
	return &NetworkTechnologyRepository{db: db}
}

// CreateTable creates the network_technologies table with lowercase column names.
func (r *NetworkTechnologyRepository) CreateTable() error {
	_, err := r.db.Exec(CreateNetworkTechnologiesTable)
	if err != nil {
		return fmt.Errorf("failed to create network_technologies table: %w", err)
	}
	return nil
}

// Insert inserts a new network technology into the database, but does not insert if it already exists.
func (r *NetworkTechnologyRepository) Insert(networkTechnology entities.NetworkTechnology) error {
	var existingID int
	err := r.db.QueryRow(SelectNetworkTechnologiesByName, networkTechnology.Name).Scan(&existingID)
	if err == nil {
		log.Printf("Network technology with name %s already exists, skipping insert.\n", networkTechnology.Name)
		return nil
	}

	if err != sql.ErrNoRows {
		return fmt.Errorf("failed to check for existing network technology: %w", err)
	}

	_, err = r.db.Exec(InsertNetworkTechnology, networkTechnology.Name, networkTechnology.Description)
	if err != nil {
		return fmt.Errorf("failed to insert network technology: %w", err)
	}

	return nil
}

// GetAll retrieves all network technologies from the database.
func (r *NetworkTechnologyRepository) GetAll() ([]entities.NetworkTechnology, error) {
	rows, err := r.db.Query(SelectAllNetworkTechnologies)
	if err != nil {
		return nil, fmt.Errorf("failed to query network_technologies: %w", err)
	}
	defer rows.Close()

	var technologies []entities.NetworkTechnology
	for rows.Next() {
		var tech entities.NetworkTechnology
		if err := rows.Scan(&tech.ID, &tech.Name, &tech.Description); err != nil {
			return nil, fmt.Errorf("failed to scan row into networkTechnology: %w", err)
		}
		technologies = append(technologies, tech)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error occurred during row iteration: %w", err)
	}

	return technologies, nil
}
