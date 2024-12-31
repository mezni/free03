package boltstore

import (
	"errors"
	"go.etcd.io/bbolt"
	"os"
	"path/filepath"
)

// BoltDBConfig holds the configuration for BoltDB operations.
type BoltDBConfig struct {
	db *bbolt.DB // The internal reference to the database instance
}

// NewBoltDBConfig initializes and returns a new instance of BoltDBConfig.
func NewBoltDBConfig() *BoltDBConfig {
	return &BoltDBConfig{}
}

// Open opens the database file with the given path.
func (cfg *BoltDBConfig) Open(dbPath string) error {
	// Extract the base name of the file (without the directory part)
	baseName := filepath.Base(dbPath)

	// Check if the database file exists
	if _, err := os.Stat(dbPath); os.IsNotExist(err) {
		return errors.New("database file '" + baseName + "' does not exist")
	}

	// Open the database file with read-write permissions
	db, err := bbolt.Open(dbPath, 0600, nil)
	if err != nil {
		return errors.New("error opening database '" + baseName + "': " + err.Error())
	}

	cfg.db = db
	return nil
}

// Create creates the database file if it does not exist and opens it.
func (cfg *BoltDBConfig) Create(dbPath string) error {
	// Extract the base name of the file (without the directory part)
	baseName := filepath.Base(dbPath)

	// Extract the directory part of dbPath
	dir := filepath.Dir(dbPath)

	// Ensure the directory exists before creating the database file
	if err := os.MkdirAll(dir, 0755); err != nil {
		return errors.New("error creating directory for database: " + err.Error())
	}

	// Check if the database file already exists
	if _, err := os.Stat(dbPath); err == nil {
		return errors.New("database file '" + baseName + "' already exists")
	}

	// Create and open the database file with read-write permissions
	db, err := bbolt.Open(dbPath, 0600, nil)
	if err != nil {
		return errors.New("error creating/opening database '" + baseName + "': " + err.Error())
	}

	cfg.db = db
	return nil
}

// Close safely closes the database when done.
func (cfg *BoltDBConfig) Close() error {
	// Ensure the database is not nil and can be closed safely
	if cfg.db == nil {
		return errors.New("no database connection to close")
	}

	// Close the database connection
	if err := cfg.db.Close(); err != nil {
		return errors.New("error closing database: " + err.Error())
	}

	cfg.db = nil
	return nil
}
