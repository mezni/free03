package main

import (
	"fmt"
	//	"github.com/mezni/expenses-go/internal/application/services"
	"github.com/mezni/expenses-go/internal/application/services"
	"github.com/mezni/expenses-go/internal/infrastructure/persistance/sqlite"
	"log"
)

func main() {
	fmt.Println("- start")
	db, err := sqlite.NewSQLiteDB("./_expenses.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	err = sqlite.Init(db)
	if err != nil {
		log.Fatal(err)
	}
	repo := sqlite.NewSQLiteOrgrRepository(db)

	service := services.NewExpenseService(repo)

	err = service.LoadExpense("./data/_data.csv")
	fmt.Println(err)

}
