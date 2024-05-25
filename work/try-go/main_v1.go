package main

import (
	"fmt"
	"github.com/google/uuid"
)

type ID string

func NewID() ID {
	return ID(uuid.NewString())
}

type Portfolio struct {
	ID      ID
	Name    string
	OwnerID ID
}

func NewPortfolio(name string, ownerID ID) Portfolio {
	return Portfolio{
		ID:      NewID(),
		Name:    name,
		OwnerID: ownerID,
	}
}

func main() {
	fmt.Println("Start")
	p := NewPortfolio("Test", NewID())
	fmt.Println(p)
}
