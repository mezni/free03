package sqlite

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
)

var createTables []string

func NewSQLiteDB(dataSourceName string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", dataSourceName)
	return db, err
}

//func CreateTable(db *sql.DB,createStmt string) ( error) {
//	_, err := db.Exec(createStmt)
//	return err
//}

func TableCreateAll(db *sql.DB) error {
	createTables := []string{
		`CREATE TABLE IF NOT EXISTS services (
            service_id TEXT PRIMARY KEY,
            service_name TEXT NOT NULL
        );`,
		`CREATE TABLE IF NOT EXISTS expenses (
            expense_id TEXT PRIMARY KEY,
            service_id TEXT NOT NULL,
            amount TEXT NOT NULL           
        );`}
	for _, query := range createTables {
		_, err := db.Exec(query)
		if err != nil {
			return err
		}
	}
	return nil
}
