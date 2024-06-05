package sqlite

import (
	"database/sql"
	"errors"
	//	"time"

	//	"github.com/google/uuid"
	_ "github.com/mattn/go-sqlite3"
	"github.com/mezni/expenses-go/internal/domain/entities"
	// "github.com/mezni/expenses-go/internal/infrastructure/persistance/sqlite"
)

type SQLiteOrgRepository struct {
	db *sql.DB
}

func NewSQLiteOrgRepository(db *sql.DB) *SQLiteOrgRepository {
	return &SQLiteOrgRepository{db: db}
}

func (r *SQLiteOrgRepository) FindByName(name string) (*entities.Org, error) {
	var org entities.Org

	row := r.db.QueryRow("SELECT id, org_name FROM orgs WHERE org_name = ?", name)

	err := row.Scan(&org.ID, &org.Name)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, errors.New("org not found")
		}
		return nil, err
	}
	return &org, nil
}
