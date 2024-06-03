package main

import (
	"fmt"
	"github.com/mezni/expenses-go/internal/infrastructure/persistance/sqlite"
	"github.com/mezni/expenses-go/internal/infrastructure/readers"
	"log"
)

func main() {
	fmt.Println("- start")
	records, err := csv.ReadCSV("./data/_data.csv")
	if err != nil {
		log.Fatalf("Failed to read CSV file: %v", err)
	}

	expenses, err := csv.ParseRecords(records)
	if err != nil {
		log.Fatalf("Failed to parse records: %v", err)
	}

	db, err := sqlite.NewSQLiteDB("./_expenses.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	//	err = sqlite.Init(db)

	//	if err != nil {
	//		log.Fatal(err)
	//	}

	repo := sqlite.NewSQLiteExpenseRepository(db)
	err = repo.Load(expenses)
	fmt.Println(err)
}
