package sqlitestore

import (
	"database/sql"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// NetworkTechnologyRepository handles database operations for network technologies.
type NetworkTechnologyRepository struct {
	db *sql.DB
}

// NewNetworkTechnologyRepository creates a new instance of NetworkTechnologyRepository.
func NewNetworkTechnologyRepository(db *sql.DB) *NetworkTechnologyRepository {
	return &NetworkTechnologyRepository{db: db}
}

// CreateTable creates the network_technologies table.
func (r *NetworkTechnologyRepository) CreateTable() error {
	query := `
		CREATE TABLE IF NOT EXISTS network_technologies (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			Name TEXT NOT NULL,
			Description TEXT NOT NULL
		)`
	_, err := r.db.Exec(query)
	return err
}

// Insert inserts a new network technology into the database.
func (r *NetworkTechnologyRepository) Insert(networkTechnology entities.NetworkTechnology) error {
	query := `
		INSERT INTO network_technologies (Name, Description) 
		VALUES (?, ?)`
	_, err := r.db.Exec(query, networkTechnology.Name, networkTechnology.Description)
	return err
}

// GetAll retrieves all network technologies from the database.
func (r *NetworkTechnologyRepository) GetAll() ([]entities.NetworkTechnology, error) {
	rows, err := r.db.Query(`
		SELECT id, Name, Description FROM network_technologies`)
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
