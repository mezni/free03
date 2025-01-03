package sqlitestore

import (
	"database/sql"
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
	query := `
		CREATE TABLE IF NOT EXISTS network_technologies (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			description TEXT NOT NULL
		)`
	_, err := r.db.Exec(query)
	return err
}

// Insert inserts a new network technology into the database, but does not insert if it already exists.
func (r *NetworkTechnologyRepository) Insert(networkTechnology entities.NetworkTechnology) error {
	// First, check if the network technology with the same name already exists.
	var existingID int
	query := `SELECT id FROM network_technologies WHERE name = ?`
	err := r.db.QueryRow(query, networkTechnology.Name).Scan(&existingID)
	if err == nil {
		// If no error, it means a record with the same name already exists. Skip the insert.
		// No error is returned, just log the action if needed
		log.Printf("Network technology with name %s already exists, skipping insert.\n", networkTechnology.Name)
		return nil // Simply return nil without inserting or throwing an error
	}

	// If the error is not nil (which is expected when no row is found), proceed to insert.
	if err != sql.ErrNoRows {
		// Return any other unexpected error
		return err
	}

	// Insert the new network technology if it doesn't already exist.
	insertQuery := `
		INSERT INTO network_technologies (name, description) 
		VALUES (?, ?)`
	_, err = r.db.Exec(insertQuery, networkTechnology.Name, networkTechnology.Description)
	return err
}

// GetAll retrieves all network technologies from the database.
func (r *NetworkTechnologyRepository) GetAll() ([]entities.NetworkTechnology, error) {
	rows, err := r.db.Query(`
		SELECT id, name, description FROM network_technologies`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var technologies []entities.NetworkTechnology
	for rows.Next() {
		var tech entities.NetworkTechnology
		if err := rows.Scan(&tech.ID, &tech.Name, &tech.Description); err != nil {
			return nil, err
		}
		technologies = append(technologies, tech)
	}
	return technologies, nil
}
