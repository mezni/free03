package sqlitestore

import (
	"database/sql"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"log"
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
	query := `
		CREATE TABLE IF NOT EXISTS network_element_types (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			description TEXT NOT NULL,
			network_technology TEXT NOT NULL
		)`
	_, err := r.db.Exec(query)
	return err
}

// Insert inserts a new network element type into the database, but does not insert if it already exists.
func (r *NetworkElementTypeRepository) Insert(networkElementType entities.NetworkElementType) error {
	// First, check if the network element type with the same name and network technology already exists.
	var existingID int
	query := `SELECT id FROM network_element_types WHERE name = ? AND network_technology = ?`
	err := r.db.QueryRow(query, networkElementType.Name, networkElementType.NetworkTechnology).Scan(&existingID)
	if err == nil {
		// If no error, it means a record with the same name and network technology already exists. Skip the insert.
		// No error is returned, just log the action if needed
		log.Printf("Network element type with name %s and network technology %s already exists, skipping insert.\n", networkElementType.Name, networkElementType.NetworkTechnology)
		return nil // Simply return nil without inserting or throwing an error
	}

	// If the error is not nil (which is expected when no row is found), proceed to insert.
	if err != sql.ErrNoRows {
		// Return any other unexpected error
		return err
	}

	// Insert the new network element type if it doesn't already exist.
	insertQuery := `
		INSERT INTO network_element_types (name, description, network_technology) 
		VALUES (?, ?, ?)`
	_, err = r.db.Exec(insertQuery, networkElementType.Name, networkElementType.Description, networkElementType.NetworkTechnology)
	return err
}

// GetAll retrieves all network element types from the database.
func (r *NetworkElementTypeRepository) GetAll() ([]entities.NetworkElementType, error) {
	rows, err := r.db.Query(`
		SELECT id, name, description, network_technology FROM network_element_types`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var elements []entities.NetworkElementType
	for rows.Next() {
		var elem entities.NetworkElementType
		if err := rows.Scan(&elem.ID, &elem.Name, &elem.Description, &elem.NetworkTechnology); err != nil {
			return nil, err
		}
		elements = append(elements, elem)
	}
	return elements, nil
}
