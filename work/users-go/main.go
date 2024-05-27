package main

import (
	"fmt"

	"github.com/google/uuid"
)

type Portfolio struct {
	ID            uuid.UUID
	Name          string
	PortfolioType string
	Limit         float64
	Parent        *uuid.UUID
}

func NewPortfolio(name string, portfolioType string, limit float64, parent *uuid.UUID) (*Portfolio, error) {
	return &Portfolio{ID: uuid.New(), Name: name, PortfolioType: portfolioType, Limit: limit, Parent: parent}, nil
}

func main() {
	p_root, _ := NewPortfolio("root", "default", 2000, nil)
	fmt.Println(p_root)
	p_it, _ := NewPortfolio("IT", "departement", 1500, &p_root.ID)
	fmt.Println(p_it)
	p_hr, _ := NewPortfolio("HR", "departement", 500, &p_root.ID)
	fmt.Println(p_hr)
	p_phonix1, _ := NewPortfolio("Phonix1", "project", 500, &p_it.ID)
	fmt.Println(p_phonix1)
	p_phonix2, _ := NewPortfolio("Phonix2", "project", 400, &p_it.ID)
	fmt.Println(p_phonix2)
	p_hr1, _ := NewPortfolio("hr1", "project", 200, &p_hr.ID)
	fmt.Println(p_hr1)
}
