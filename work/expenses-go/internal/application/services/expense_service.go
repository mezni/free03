package services

import (
	"fmt"
	//    "github.com/google/uuid"
	//	"github.com/mezni/expenses-go/internal/domain/entities"
	"encoding/csv"
	"github.com/mezni/expenses-go/internal/domain/entities"
	"github.com/mezni/expenses-go/internal/domain/repositories"
	"os"
)

type ExpenseService struct {
	repo repositories.OrgRepository
}

func NewExpenseService(repo repositories.OrgRepository) *ExpenseService {
	return &ExpenseService{repo: repo}
}

func ReadCSV(filePath string) ([][]string, error) {

	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	return records, nil
}

func contains(s []string, searchterm string) bool {
	for _, v := range s {
		if v == searchterm {
			return true
		}
	}
	return false
}

func (s *ExpenseService) ParseRecords(records [][]string) error {
	orgs := []string{}
	periods := []string{}
	providers := []string{}

	orgItems := []*entities.Org{}

	for _, r := range records[1:] {
		if contains(orgs, r[0]) == false {
			orgs = append(orgs, r[0])
		}
		if contains(periods, r[1]) == false {
			periods = append(periods, r[1])
		}
		if contains(providers, r[2]) == false {
			providers = append(providers, r[2])
		}
	}

	for _, v := range orgs {
		org, err := s.repo.FindByName(v)
		if err != nil {
			return err
		}
		orgItems = append(orgItems, org)
	}
	fmt.Println(orgItems)
	return nil
}

func (s *ExpenseService) LoadExpense(filePath string) error {

	records, err := ReadCSV(filePath)
	if err != nil {
		return err
	}
	err = s.ParseRecords(records)

	return err

}
