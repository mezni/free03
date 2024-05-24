package main

import (
	"fmt"
	"github.com/google/uuid"
	"github.com/mezni/try-go/aggregates"
)

type Test struct {
	ID      uuid.UUID
	Name    string
	OwnerID *uuid.UUID
}

func main() {
	fmt.Println("Hello World")
	p := aggregates.NewPortfolio("Test", uuid.New(), uuid.New())
	fmt.Println(p)
	x := Test{
		ID:      uuid.New(),
		Name:    "Test",
		OwnerID: nil,
	}
	fmt.Println(x)
}
