package services

import (
	"encoding/csv"
	"errors"
	"fmt"
	"github.com/mezni/expenses-go/internal/infrastructure/persistance/sqlite"
	"os"
)

type ExpenseService struct {
	repo sqlite.SQLiteOrgRepository
}

func NewExpenseService(repo sqlite.SQLiteOrgRepository) (*ExpenseService, error) {
	return &ExpenseService{repo: repo}, nil
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

func (s *ExpenseService) ParseRecords(records [][]string) (string, error) {
	//	services := []map[string]string{}
	orgs := []string{}
	periods := []string{}
	providers := []string{}
	services := []map[string]string{}
	expenses := []map[string]string{}
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
		serviceExists := false
		for _, s := range services {
			if r[2] == s["provider"] && r[3] == s["service"] {
				serviceExists = true
				break
			}
		}
		if serviceExists == false {
			services = append(services, map[string]string{"provider": r[2], "service": r[3]})
		}
		expense := map[string]string{"org": r[0], "period": r[1], "provider": r[2], "service": r[3], "cost": r[4]}
		expenses = append(expenses, expense)
	}
	for _, v := range orgs {
		x, _ := s.repo.FindByName(v)
		fmt.Println(x)
	}
	fmt.Println(periods)
	fmt.Println(providers)
	fmt.Println(services)
	fmt.Println(expenses)

	return "os", nil
}

func (s *ExpenseService) Load(fileName string) error {

	if _, err := os.Stat(fileName); errors.Is(err, os.ErrNotExist) {
		return err
	}

	records, err := ReadCSV(fileName)

	if err != nil {
		return err
	}

	expenses, err := ParseRecords(records)
	if err != nil {
		return err
	}
	fmt.Println(expenses)
	return nil
}
