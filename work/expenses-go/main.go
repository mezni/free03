package main

import (
	"fmt"
	"github.com/mezni/expenses-go/domain/entities"
	"github.com/mezni/expenses-go/infrastructure/sqlite"
	"log"
)

func main() {
	fmt.Println("- start")
	db, err := sqlite.NewSQLiteDB("./_expenses.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	err = sqlite.TablesCreateAll(db, sqlite.TablesCreateStmt)
	if err != nil {
		log.Fatal(err)
	}

	repo := sqlite.NewSQLiteServiceRepository(db)
	_ = repo.Create(entities.NewService("ec2"))
	ec2, err := repo.FindByName("ec2")
	fmt.Println(ec2, err)
}
