package sqlite

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
)

func NewSQLiteDB(dataSourceName string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", dataSourceName)
	return db, err
}

func TablesCreateAll(db *sql.DB, tablesCreateStmt []string) error {
	for _, query := range tablesCreateStmt {
		_, err := db.Exec(query)
		if err != nil {
			return err
		}
	}
	return nil
}
