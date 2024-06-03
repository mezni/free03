package sqlite

import (
	"database/sql"
	"github.com/mezni/expenses-go/internal/domain/entities"
)

type SQLiteServiceRepository struct {
	DB *sql.DB
}

func NewSQLiteServiceRepository(db *sql.DB) *SQLiteServiceRepository {
	return &SQLiteServiceRepository{DB: db}
}

func (repo *SQLiteServiceRepository) GetOrCreate() error {
}
