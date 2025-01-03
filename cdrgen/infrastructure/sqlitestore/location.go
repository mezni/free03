package sqlitestore

import (
	"log"
	"database/sql"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

type LocationRepository struct {
	db *sql.DB
}

// NewLocationRepository creates a new instance of LocationRepository.
func NewLocationRepository(db *sql.DB) *LocationRepository {
	return &LocationRepository{db: db}
}

// CreateTable creates the Location table in the database.
func (r *LocationRepository) CreateTable() error {
	query := `
	CREATE TABLE IF NOT EXISTS locations (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		latitude_min REAL NOT NULL,
		latitude_max REAL NOT NULL,
		longitude_min REAL NOT NULL,
		longitude_max REAL NOT NULL,
		area_code TEXT NOT NULL,
		network_technology TEXT NOT NULL
	);`
	_, err := r.db.Exec(query)
	return err
}

// Insert inserts a new location into the database, but does not insert if a duplicate exists based on name and network technology.
func (r *LocationRepository) Insert(location entities.Location) error {
	// First, check if the location with the same name and network technology already exists.
	var existingID int
	query := `SELECT id FROM locations WHERE name = ? AND network_technology = ?`
	err := r.db.QueryRow(query, location.Name, location.NetworkTechnology).Scan(&existingID)
	if err == nil {
		// If no error, it means a record with the same name and network technology already exists. Skip the insert.
		// No error is returned, just log the action if needed
		log.Printf("Location with name %s and network technology %s already exists, skipping insert.\n", location.Name, location.NetworkTechnology)
		return nil // Simply return nil without inserting or throwing an error
	}

	// If the error is not nil (which is expected when no row is found), proceed to insert.
	if err != sql.ErrNoRows {
		// Return any other unexpected error
		return err
	}

	// Insert the new location if it doesn't already exist.
	insertQuery := `
		INSERT INTO locations (name, latitude_min, latitude_max, longitude_min, longitude_max, area_code, network_technology)
		VALUES (?, ?, ?, ?, ?, ?, ?);`
	_, err = r.db.Exec(insertQuery,
		location.Name, location.LatitudeMin, location.LatitudeMax,
		location.LongitudeMin, location.LongitudeMax, location.AreaCode,
		location.NetworkTechnology,
	)
	return err
}


// GetAll retrieves all locations from the database.
func (r *LocationRepository) GetAll() ([]entities.Location, error) {
	rows, err := r.db.Query(`
	SELECT id, name, latitude_min, latitude_max, longitude_min, longitude_max, area_code, network_technology
	FROM locations;`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var locations []entities.Location
	for rows.Next() {
		var location entities.Location
		if err := rows.Scan(&location.ID, &location.Name, &location.LatitudeMin, &location.LatitudeMax,
			&location.LongitudeMin, &location.LongitudeMax, &location.AreaCode, &location.NetworkTechnology); err != nil {
			return nil, err
		}
		locations = append(locations, location)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return locations, nil
}
