package main

import (
	"fmt"
	"github.com/mezni/expenses-go/internal/infrastructure/sqlite"
	"log"
)

type ExpenseRecord struct {
	OrgName      string
	PeriodName   string
	ProviderName string
	ServiceName  string
	Cost         float64
}

var expenses = []*ExpenseRecord{
	&ExpenseRecord{"momentum", "2024-05-20", "aws", "ec2", 1.51},
	&ExpenseRecord{"momentum", "2024-05-20", "aws", "s3", 1.79},
	&ExpenseRecord{"momentum", "2024-05-20", "aws", "lambda", 0.71},
	&ExpenseRecord{"momentum", "2024-05-21", "aws", "ec2", 1.51},
	&ExpenseRecord{"momentum", "2024-05-21", "aws", "s3", 1.79},
	&ExpenseRecord{"momentum", "2024-05-21", "aws", "lambda", 0.71},
}

func main() {
	fmt.Println("- start")

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
	for _, v := range expenses {
		fmt.Println(v)
	}
}
