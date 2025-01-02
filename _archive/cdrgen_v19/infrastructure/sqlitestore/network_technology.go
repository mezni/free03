package sqlitestore

import (
	"database/sql"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// NetworkTechnologyRepository implements the NetworkTechnologyRepository interface using SQLite.
type NetworkTechnologyRepository struct {
	DB *sql.DB
}

// NewNetworkTechnologyRepository creates a new NetworkTechnologyRepository with the given database file path.
func NewNetworkTechnologyRepository(dbFilePath string) (*NetworkTechnologyRepository, error) {
	db, err := sql.Open("sqlite3", dbFilePath)
	if err != nil {
		return nil, fmt.Errorf("could not open database: %v", err)
	}

	// Initialize the schema (create tables if they don't exist)
	_, err = db.Exec(`
	CREATE TABLE IF NOT EXISTS network_technologies (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		description TEXT NOT NULL
	);`)
	if err != nil {
		return nil, fmt.Errorf("could not initialize schema: %v", err)
	}

	return &NetworkTechnologyRepository{DB: db}, nil
}

// Save saves a NetworkTechnology to the database (insert or update).
func (repo *NetworkTechnologyRepository) Save(technology entities.NetworkTechnology) error {
	if technology.ID == 0 {
		// Insert a new technology
		_, err := repo.DB.Exec("INSERT INTO network_technologies (name, description) VALUES (?, ?)", technology.Name, technology.Description)
		return err
	}
	// Update an existing technology
	_, err := repo.DB.Exec("UPDATE network_technologies SET name = ?, description = ? WHERE id = ?", technology.Name, technology.Description, technology.ID)
	return err
}

// GetAll retrieves all network technologies from the database.
func (repo *NetworkTechnologyRepository) GetAll() ([]entities.NetworkTechnology, error) {
	rows, err := repo.DB.Query("SELECT id, name, description FROM network_technologies")
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
