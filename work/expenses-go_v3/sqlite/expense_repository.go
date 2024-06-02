package sqlite

import (
	"database/sql"
	"github.com/mezni/expenses-go/domain"
	// "errors"
	// "github.com/google/uuid"
)

type SQLiteExpenseRepository struct {
	db *sql.DB
}

func NewSQLiteExpenseRepository(db *sql.DB) *SQLiteExpenseRepository {
	return &SQLiteExpenseRepository{db: db}
}

func (r *SQLiteExpenseRepository) SaveService(service *domain.Service) error {
	tx, err := r.db.Begin()
	if err != nil {
		return err
	}

	_, err = tx.Exec("INSERT INTO services ( service_name) VALUES (?)",
		service.ID, service.Name)
	if err != nil {
		tx.Rollback()
		return err
	}
	tx.Commit()
	return nil
}
