package sqlite

import (
	"database/sql"
	"github.com/google/uuid"
	_ "github.com/mattn/go-sqlite3"
)

var tablesCreateStmt = []string{
	`CREATE TABLE IF NOT EXISTS orgs (
            id TEXT PRIMARY KEY,
            org_name TEXT NOT NULL
        );`,
	`CREATE TABLE IF NOT EXISTS providers (
            id TEXT PRIMARY KEY,
            provider_name TEXT NOT NULL
        );`,
	`CREATE TABLE IF NOT EXISTS services (
            id TEXT PRIMARY KEY,
            service_name TEXT NOT NULL,
            provider_id TEXT NOT NULL,
            FOREIGN KEY (provider_id) REFERENCES providers(id)
        );`,
	`CREATE TABLE IF NOT EXISTS expenses (
            id TEXT PRIMARY KEY,
            provider_id TEXT NOT NULL,
            service_id TEXT NOT NULL,
            amount INTEGER NOT NULL,
            FOREIGN KEY (provider_id) REFERENCES providers(id),
            FOREIGN KEY (service_id) REFERENCES services(id)
        );`}

func NewSQLiteDB(dataSourceName string) (*sql.DB, error) {
	db, err := sql.Open("sqlite3", dataSourceName)
	if err != nil {
		return nil, err
	}
	err = TablesCreateAll(db, tablesCreateStmt)
	if err != nil {
		return nil, err
	}
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

func Init(db *sql.DB) error {
	tx, err := db.Begin()
	if err != nil {
		return err
	}

	_, err = tx.Exec("INSERT INTO orgs (id, org_name) VALUES (?, ?)", uuid.New(), "momentum")
	if err != nil {
		tx.Rollback()
		return err
	}
	_, err = tx.Exec("INSERT INTO providers (id, provider_name) VALUES (?, ?)", uuid.New(), "aws")
	if err != nil {
		tx.Rollback()
		return err
	}
	tx.Commit()
	return nil
}
