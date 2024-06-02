package main

import (
	"fmt"
	"github.com/mezni/expenses-go/internal/infrastructure/sqlite"
	"log"
)

type ExpenseRecord struct {
	OrgName      string
	ProviderName string
	ServiceName  string
	Cost         float64
}

func main() {
	fmt.Println("- start")
	expenses := []*ExpenseRecord{
		&ExpenseRecord{"momentum", "aws", "ec2", 1.71},
		&ExpenseRecord{"momentum", "aws", "s3", 1.71},
		&ExpenseRecord{"momentum", "aws", "lambda", 1.71},
	}
	fmt.Println(expenses[0])
	db, err := sqlite.NewSQLiteDB("./_expenses.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	// err = sqlite.Init(db)
	//
	//	if err != nil {
	//		log.Fatal(err)
	//	}
}
