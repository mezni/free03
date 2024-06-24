package main

import (
	"fmt"
	"github.com/mezni/users-go/internal/domain/entities"
)

func main() {
	u := entities.NewUser("dali")
	fmt.Println(u)
	u.UpdateName("dali1")
	fmt.Println(u)
}
