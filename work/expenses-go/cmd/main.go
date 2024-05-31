package main

import (
	"fmt"
	"github.com/mezni/expenses-go/internal/domain"
)

func main() {
	fmt.Println("- start")
	e := domain.Expense{1, "DD", 1.0}
	fmt.Println(e)
}
