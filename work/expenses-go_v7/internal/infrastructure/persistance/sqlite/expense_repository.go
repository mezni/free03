package sqlite

import (
	"database/sql"
	"fmt"
	"github.com/mezni/expenses-go/internal/domain/entities"
	"github.com/mezni/expenses-go/internal/infrastructure/readers"
)

func contains(s []string, searchterm string) bool {
	for _, v := range s {
		if v == searchterm {
			return true
		}
	}
	return false
}

type SQLiteExpenseRepository struct {
	DB *sql.DB
}

func NewSQLiteExpenseRepository(db *sql.DB) *SQLiteExpenseRepository {
	return &SQLiteExpenseRepository{DB: db}
}

func (repo *SQLiteExpenseRepository) Load(expenses []*csv.ExpenseRecord) error {
	orgs := []string{}
	periods := []string{}
	providers := []string{}
	services := []string{}
	for _, v := range expenses {

		if contains(orgs, v.OrgName) == false {
			orgs = append(orgs, v.OrgName)
		}
		if contains(periods, v.PeriodName) == false {
			periods = append(periods, v.PeriodName)
		}
		if contains(providers, v.ProviderName) == false {
			providers = append(providers, v.ProviderName)
		}
		if contains(services, v.ServiceName) == false {
			services = append(services, v.ServiceName)
		}
	}

	fmt.Println(periods)
	fmt.Println(providers)
	fmt.Println(services)
	for _, v := range orgs {
		row := repo.DB.QueryRow("SELECT id, org_name FROM orgs WHERE org_name = ?", v)
		org := &domain.Org{}
		err := row.Scan(&org.ID, &org.Name)
		if err != nil {
			return err
		}
		fmt.Println(org)
	}
	return nil
}

//func (repo *SQLiteUserRepository) GetByID(id int) (*domain.Expense, error) {
//	row := repo.DB.QueryRow("SELECT id, name, email FROM users WHERE id = ?", id)
//	user := &domain.User{}
//	err := row.Scan(&user.ID, &user.Name, &user.Email)
//	if err != nil {
//		return nil, err
//	}
//	return user, nil
//}
