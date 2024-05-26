package main

import (
	"fmt"
	"github.com/mezni/users-go/domain"
	"github.com/mezni/users-go/infrastructure/persistance/memory"
)

func main() {
	fmt.Println("start -")
	p := entities.NewPortfolio("test", 0)
	p.UpdateName("Test")
	fmt.Println(p)

	r := memory.NewInMemoryPortfolioRepository()
	print(r)
	fmt.Println("end -")
}
