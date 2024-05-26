package main

import (
	"fmt"
	"github.com/mezni/users-go/domain/aggregates"
)

func main() {
	fmt.Println("- start")
	p, _ := aggregates.NewPortfolio("Test")
	fmt.Println(p)
	p.SetName("Test2")
	p.SetLimit(12)
	fmt.Println(p)
	fmt.Println(p.Limit)
	fmt.Println("- end")
}
