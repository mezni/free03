package main

import (
	"fmt"
	"github.com/mezni/expenses-go/sqlite"
	"log"
)

func main() {
	fmt.Println("- start")
	db, err := sqlite.NewSQLiteDB("./_expenses.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()
	err = sqlite.TableCreateAll(db)
	if err != nil {
		log.Fatal(err)
	}
	//		a := `CREATE TABLE IF NOT EXISTS services (
	//	           service_id TEXT PRIMARY KEY,
	//	           service_name TEXT NOT NULL
	//	       );`
	//		err = sqlite.CreateTable(db, a)
	//		if err != nil {
	//			log.Fatal(err)
	//		}
}
