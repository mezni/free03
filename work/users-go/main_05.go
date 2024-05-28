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

type Node struct {
	id        uuid.UUID
	portfolio *Portfolio
	Children  []*Node
}

type Tree struct {
	root *Node
}

func (t *Tree) AddNode(p *Portfolio) {
	if p.Parent == nil {
		t.root = &Node{p.ID, p, nil}
	}
}

func main() {
	t := Tree{}
	fmt.Println(t)
	p, _ := NewPortfolio("Test", "root", 2000, nil)
	t.AddNode(p)
	fmt.Println(t.root.portfolio)
}
