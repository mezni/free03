package csv

import (
	"encoding/csv"
	"os"
	"strconv"
)

type ExpenseRecord struct {
	OrgName      string
	PeriodName   string
	ProviderName string
	ServiceName  string
	Cost         float64
}

func NewExpenseRecord(orgName, periodName, providerName, serviceName string, cost float64) *ExpenseRecord {
	return &ExpenseRecord{orgName, periodName, providerName, serviceName, cost}
}

func ReadCSV(filePath string) ([][]string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	reader := csv.NewReader(file)
	records, err := reader.ReadAll()
	if err != nil {
		return nil, err
	}

	return records, nil
}

func ParseRecords(records [][]string) ([]*ExpenseRecord, error) {
	var expenses []*ExpenseRecord
	for _, record := range records[1:] { // Skip the header row
		orgName := record[0]
		periodName := record[1]
		providerName := record[2]
		serviceName := record[3]
		cost, _ := strconv.ParseFloat(record[4], 64)
		expense := NewExpenseRecord(orgName, periodName, providerName, serviceName, cost)
		expenses = append(expenses, expense)
	}

	return expenses, nil
}
