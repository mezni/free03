package main

import (
	"database/sql"
	"fmt"
	"github.com/google/uuid"
	_ "github.com/mattn/go-sqlite3"
	"log"
)

func main() {
	fmt.Println("- start")
	db, err := sql.Open("sqlite3", "./_resources.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	_, err = db.Exec(`CREATE TABLE IF NOT EXISTS resources (
		id TEXT PRIMARY KEY,
		name TEXT
	)`)
	if err != nil {
		log.Fatal(err)
	}

	tx, err := db.Begin()
	if err != nil {
		log.Fatal(err)
	}
	_, err = tx.Exec("INSERT INTO resources (id, name) VALUES (?, ?)", uuid.New().String(), "TEST")
	if err != nil {
		tx.Rollback()
		log.Fatal(err)
	}
	tx.Commit()

	row, err := db.Query("SELECT id,name FROM resources")
	if err != nil {
		log.Fatal(err)
	}
	defer row.Close()
	for row.Next() { // Iterate and fetch the records from result cursor
		var id string
		var name string
		row.Scan(&id, &name)
		log.Println(id, name)
	}
}
