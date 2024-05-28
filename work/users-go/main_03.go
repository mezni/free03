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

type PortfolioInput struct {
	Name          string
	PortfolioType string
	Limit         float64
	Parent        string
}

type Node struct {
	id        uuid.UUID
	portfolio *Portfolio
	Children  []*Node
}

type Tree struct {
	root *Node
}

func NewNode(p Portfolio) *Portfolio {
	return &Node{id: p.ID, portfolio: *p}
}

func main() {
	portfolios := Tree{}
	fmt.Println(portfolios)
	//	portfolios := &Node{}
	portfolioInput := []PortfolioInput{
		{"root", "default", 2000, ""},
		{"IT", "department", 1500, "root"},
		{"HR", "department", 1000, "root"},
		{"team1", "team", 1000, "IT"},
		{"team2", "team", 500, "IT"},
		{"phonix1", "project", 500, "IT"},
		{"phonix2", "project", 500, "IT"},
		{"hr1", "project", 300, "IT"},
	}
	for _, v := range portfolioInput {
		if v.Parent == "" {
			p, _ := NewPortfolio(v.Name, v.PortfolioType, v.Limit, nil)
			//			child := &TreeNode{id: p.ID, portfolio:p}
			n := NewNode(p)
			fmt.Println(n)
		}
	}
	fmt.Println(portfolios)
}
