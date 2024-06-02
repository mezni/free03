package sqlite

import (
	"database/sql"
	"errors"

	"github.com/google/uuid"
	"github.com/mezni/expenses-go/domain/entities"
)

type SQLiteServiceRepository struct {
	db *sql.DB
}

func NewSQLiteServiceRepository(db *sql.DB) *SQLiteServiceRepository {
	return &SQLiteServiceRepository{db: db}
}

func (r *SQLiteServiceRepository) Create(service *entities.Service) error {
	tx, err := r.db.Begin()
	if err != nil {
		return err
	}

	_, err = tx.Exec("INSERT INTO services (service_id, service_name) VALUES (?, ?)",
		service.ID, service.Name)
	if err != nil {
		tx.Rollback()
		return err
	}
	tx.Commit()
	return nil
}

func (r *SQLiteServiceRepository) FindByID(id uuid.UUID) (*entities.Service, error) {
	var service entities.Service
	service.ID = id
	row := r.db.QueryRow("SELECT  service_name FROM services WHERE service_id = ?", id)
	err := row.Scan(&service.Name)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, errors.New("service not found")
		}
		return nil, err
	}
	return &service, nil
}

func (r *SQLiteServiceRepository) FindByName(name string) (*entities.Service, error) {
	var service entities.Service
	service.Name = name
	row := r.db.QueryRow("SELECT  service_id FROM services WHERE service_name = ?", name)
	err := row.Scan(&service.ID)
	if err != nil {
		if err == sql.ErrNoRows {
			return nil, errors.New("service not found")
		}
		return nil, err
	}
	return &service, nil
}
