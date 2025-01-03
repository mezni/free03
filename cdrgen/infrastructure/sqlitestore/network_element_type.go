package sqlitestore

import (
	"database/sql"
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

// CreateTable creates the network_element_types table.
func (r *NetworkElementTypeRepository) CreateTable() error {
	query := `
		CREATE TABLE IF NOT EXISTS network_element_types (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			Name TEXT NOT NULL,
			Description TEXT NOT NULL,
			NetworkTechnology TEXT NOT NULL
		)`
	_, err := r.db.Exec(query)
	return err
}

// Insert inserts a new network element type into the database.
func (r *NetworkElementTypeRepository) Insert(networkElementType entities.NetworkElementType) error {
	query := `
		INSERT INTO network_element_types (Name, Description, NetworkTechnology) 
		VALUES (?, ?, ?)`
	_, err := r.db.Exec(query, networkElementType.Name, networkElementType.Description, networkElementType.NetworkTechnology)
	return err
}

// GetAll retrieves all network element types from the database.
func (r *NetworkElementTypeRepository) GetAll() ([]entities.NetworkElementType, error) {
	rows, err := r.db.Query(`
		SELECT id, Name, Description, NetworkTechnology FROM network_element_types`)
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
