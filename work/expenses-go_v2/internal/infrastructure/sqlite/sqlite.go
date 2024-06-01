package sqlite

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
)

func NewSQLiteDB(dataSourceName string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", dataSourceName)
	if err != nil {
		return db, err
	}
	return db, nil
}
