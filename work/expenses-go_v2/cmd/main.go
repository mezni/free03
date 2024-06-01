package main

import (
	"fmt"
	"github.com/mezni/expenses-go/internal/infrastructure/sqlite"
	"log"
)

//momentum tech,2023-11-01,aws,367475994817,367475994817,Tax,,,,,,,,,,[],,54.41,USD

type ExpenseInput struct {
	Org      string
	Period   string
	Provider string
	Account  string
	Service  string
	Cost     float64
	Currency string
}

func contains(s []string, searchterm string) bool {
	for _, v := range s {
		if v == searchterm {
			return true
		}
	}
	return false
}

func main() {
	fmt.Println("- start")
	exspenses := []*ExpenseInput{
		&ExpenseInput{"momentum tech", "2024-05-20", "aws", "367475994817", "ec2", 2.51, "USD"},
		&ExpenseInput{"momentum tech", "2024-05-20", "aws", "367475994817", "s3", 4.75, "USD"},
		&ExpenseInput{"momentum tech", "2024-05-21", "aws", "367475994817", "ec2", 1.91, "USD"},
		&ExpenseInput{"momentum tech", "2024-05-21", "aws", "367475994817", "s3", 4.76, "USD"},
	}
	orgs := []string{}
	periods := []string{}
	for _, v := range exspenses {
		if contains(orgs, v.Org) == false {
			orgs = append(orgs, v.Org)
		}
		if contains(periods, v.Period) == false {
			periods = append(periods, v.Period)
		}
	}
	fmt.Println(orgs)
	fmt.Println(periods)

	db, err := sqlite.NewSQLiteDB("_expenses.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	createTables := []string{
		`CREATE TABLE IF NOT EXISTS orgs (
            id TEXT PRIMARY KEY,
            org_name TEXT NOT NULL
        );`}
	for _, query := range createTables {
		_, err := db.Exec(query)
		if err != nil {
			log.Fatalf("Failed to create table: %v", err)
		}
	}
}
