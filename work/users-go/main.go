package main

import (
	"fmt"
	"github.com/mezni/users-go/memrepo"
	"github.com/mezni/users-go/services"
	//	"time"
)

func main() {
	fmt.Println("- start")
	repo := memory_repo.NewInMemoryPortfolioRepository()
	service := services.NewPortfolioService(repo)
	fmt.Println(repo)
	service.AddPortfolio("Test")
	service.AddPortfolio("Test1")
	fmt.Println(repo)
	fmt.Println("- end")
}
