package main

import (
	"fmt"
	//	"os"
	"time"
)

type InputRecord map[string]string

type csvReader struct {
	filePath string
}

type CSVReader interface {
	Read() ([]InputRecord, error)
}

func (r *csvReader) Read() ([]InputRecord, error) {
	return nil, nil
}

func NewCSVReader(filePath string) CSVReader {
	return &csvReader{filePath: filePath}
}

func main() {
	filePath := "data.csv"
	fmt.Printf("%s - start \n", time.Now().Format("2006-01-02 15:04:05"))
	csvReader := file.NewCSVReader(filePath)
	fmt.Printf("%s - end  \n", time.Now().Format("2006-01-02 15:04:05"))
}
