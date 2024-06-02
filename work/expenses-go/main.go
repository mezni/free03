package main

import (
	"fmt"
	"github.com/mezni/expenses-go/internal/infrastructure/sqlite"
	"log"
)

type ExpenseRecord struct {
	ProviderName string
	ServiceName  string
	Cost         float64
}

func main() {
	fmt.Println("- start")
	expenses := []*ExpenseRecord{
		&ExpenseRecord{"aws", "ec2", 1.71},
		&ExpenseRecord{"aws", "s3", 1.71},
		&ExpenseRecord{"aws", "lambda", 1.71},
	}
	fmt.Println(expenses[0])
	db, err := sqlite.NewSQLiteDB("./_expenses.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
}
