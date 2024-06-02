package main

import (
	"fmt"
	"github.com/mezni/expenses-go/internal/infrastructure/readers"
	"log"
)

func main() {
	fmt.Println("- start")
	records, err := csv.ReadCSV("./data/data.csv")
	if err != nil {
		log.Fatalf("Failed to read CSV file: %v", err)
	}

	expenses, err := csv.ParseRecords(records)
	if err != nil {
		log.Fatalf("Failed to parse records: %v", err)
	}
}
