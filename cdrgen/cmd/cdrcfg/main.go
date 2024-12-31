package main

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/application/services"
	"log"
)

func main() {
	// Provide paths to the config file and database file
	initService := services.NewInitDBService("baseline.json", "config.db")

	// Initialize the database
	err := initService.InitializeDB()
	if err != nil {
		log.Fatal(err)
	}

	// Your application logic here
	fmt.Println("Database initialized and ready for use.")
}
