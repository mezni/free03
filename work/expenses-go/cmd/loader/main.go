package main

import (
	"fmt"
	//	"github.com/mezni/expenses-go/internal/application/services"
	"github.com/mezni/expenses-go/internal/infrastructure/persistance/sqlite"
	"github.com/mezni/expenses-go/internal/application/services"
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
	fmt.Println(repo)
	
	service :=services.NewExpenseService(repo)
	fmt.Println(service)
	
	err=service.Load()
	fmt.Println(err)

}
