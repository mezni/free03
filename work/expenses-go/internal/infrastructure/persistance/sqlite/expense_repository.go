package sqlite

import (
	"database/sql"
	"github.com/mezni/expenses-go/internal/domain"
)

type SQLiteExpenseRepository struct {
	DB *sql.DB
}

func NewSQLiteExpenseRepository(db *sql.DB) *SQLiteExpenseRepository {
	return &SQLiteExpenseRepository{DB: db}
}

func (repo *SQLiteUserRepository) GetByID(id int) (*domain.Expense, error) {
	row := repo.DB.QueryRow("SELECT id, name, email FROM users WHERE id = ?", id)
	user := &domain.User{}
	err := row.Scan(&user.ID, &user.Name, &user.Email)
	if err != nil {
		return nil, err
	}
	return user, nil
}
