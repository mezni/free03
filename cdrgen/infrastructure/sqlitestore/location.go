package sqlitestore

import (
	"database/sql"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"log"
)

// LocationRepository handles database operations for locations.
type LocationRepository struct {
	db *sql.DB
}

// NewLocationRepository creates a new instance of LocationRepository.
func NewLocationRepository(db *sql.DB) *LocationRepository {
	return &LocationRepository{db: db}
}

// CreateTable creates the locations table.
func (r *LocationRepository) CreateTable() error {
	_, err := r.db.Exec(CreateLocationsTable)
	if err != nil {
		return fmt.Errorf("failed to create locations table: %w", err)
	}
	return nil
}

// Insert inserts a new location into the database, avoiding duplicates by name and technology.
func (r *LocationRepository) Insert(location entities.Location) error {
	var existingID int
	err := r.db.QueryRow(SelectLocationsByNameAndTech, location.Name, location.NetworkTechnology).Scan(&existingID)
	if err == nil {
		log.Printf("Location with name %s and network technology %s already exists, skipping insert.\n", location.Name, location.NetworkTechnology)
		return nil
	}

	if err != sql.ErrNoRows {
		return fmt.Errorf("failed to check for existing location: %w", err)
	}

	_, err = r.db.Exec(InsertLocation, location.Name, location.LatitudeMin, location.LatitudeMax, location.LongitudeMin, location.LongitudeMax, location.AreaCode, location.NetworkTechnology)
	if err != nil {
		return fmt.Errorf("failed to insert location: %w", err)
	}

	return nil
}

// GetAll retrieves all locations from the database.
func (r *LocationRepository) GetAll() ([]entities.Location, error) {
	rows, err := r.db.Query(SelectAllLocations)
	if err != nil {
		return nil, fmt.Errorf("failed to query locations: %w", err)
	}
	defer rows.Close()

	var locations []entities.Location
	for rows.Next() {
		var loc entities.Location
		if err := rows.Scan(&loc.ID, &loc.Name, &loc.LatitudeMin, &loc.LatitudeMax, &loc.LongitudeMin, &loc.LongitudeMax, &loc.AreaCode, &loc.NetworkTechnology); err != nil {
			return nil, fmt.Errorf("failed to scan row into location: %w", err)
		}
		locations = append(locations, loc)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error occurred during row iteration: %w", err)
	}

	return locations, nil
}
