package sqlitestore

import (
	"database/sql"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// NetworkElementTypeRepository implements the NetworkElementTypeRepository interface using SQLite.
type NetworkElementTypeRepository struct {
	DB *sql.DB
}

// NewNetworkElementTypeRepository creates a new NetworkElementTypeRepository with the given database file path.
func NewNetworkElementTypeRepository(db *sql.DB) *NetworkElementTypeRepository {
	return &NetworkElementTypeRepository{
		DB: db,
	}
}

// Save saves a NetworkElement to the database.
func (repo *NetworkElementTypeRepository) Save(element entities.NetworkElementType) error {
	_, err := repo.DB.Exec("INSERT INTO network_elements (name, description, network_technology) VALUES (?, ?, ?)", element.Name, element.Description, element.NetworkTechnology)
	return err
}

// GetAll retrieves all network elements from the database.
func (repo *NetworkElementTypeRepository) GetAll() ([]entities.NetworkElementType, error) {
	rows, err := repo.DB.Query("SELECT id, name, description, network_technology FROM network_elements")
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var elements []entities.NetworkElementType
	for rows.Next() {
		var elem entities.NetworkElement
		if err := rows.Scan(&elem.ID, &elem.Name, &elem.Description, &elem.NetworkTechnology); err != nil {
			return nil, err
		}
		elements = append(elements, elem)
	}

	return elements, nil
}
