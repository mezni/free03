package sqlitestore

import (
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
		area_code INTEGER NOT NULL,
		network_technology TEXT NOT NULL
	);`
	_, err := r.db.Exec(query)
	return err
}

// Insert inserts a new location into the database.
func (r *LocationRepository) Insert(location entities.Location) error {
	query := `
	INSERT INTO locations (name, latitude_min, latitude_max, longitude_min, longitude_max, area_code, network_technology)
	VALUES (?, ?, ?, ?, ?, ?, ?);`
	_, err := r.db.Exec(query,
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
