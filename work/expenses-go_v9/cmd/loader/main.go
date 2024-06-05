package main

import (
	"fmt"
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
	//	err = sqlite.Init(db)
	//	if err != nil {
	//		log.Fatal(err)
	//	}

	orgRepo, err := sqlite.NewSQLiteOrgRepository(db)

	loadService, err := services.NewExpenseService(orgRepo)
	err = loadService.Load("./data/_data.csv")
	fmt.Println(err)
}
