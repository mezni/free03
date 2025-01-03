package sqlitestore

import (
	"database/sql"
	"log"

	_ "github.com/mattn/go-sqlite3" 
)

// OpenDatabase opens a database connection and verifies it.
func OpenDatabase(dbFile string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", dbFile)
	if err != nil {
		return nil, err
	}

	// Verify the connection
	if err := db.Ping(); err != nil {
		return nil, err
	}

	log.Println("Database connection opened successfully")
	return db, nil
}

// CloseDatabase closes the given database connection.
func CloseDatabase(db *sql.DB) error {
	if db != nil {
		err := db.Close()
		if err != nil {
			return err
		}
		log.Println("Database connection closed successfully")
	}
	return nil
}
