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

func generate() []*Portfolio {
	var portfolios []*Portfolio
	portfolioInput := []PortfolioInput{
		{"root", "default", 3000, ""},
		{"IT", "department", 2000, "root"},
		{"HR", "department", 500, "root"},
		{"Sales", "department", 500, "root"},
		{"team1", "team", 1000, "IT"},
		{"team2", "team", 500, "IT"},
		{"phonix1", "project", 500, "team1"},
		{"phonix2", "project", 500, "team1"},
		{"phonix3", "project", 500, "team2"},
		{"hr1", "project", 300, "HR"},
	}
	for _, v := range portfolioInput {
		if v.Parent == "" {
			p, _ := NewPortfolio(v.Name, v.PortfolioType, v.Limit, nil)
			portfolios = append(portfolios, p)
		} else {
			for _, p := range portfolios {
				if v.Parent == p.Name {
					parentID := p.ID
					p, _ := NewPortfolio(v.Name, v.PortfolioType, v.Limit, &parentID)
					portfolios = append(portfolios, p)
					break
				}
			}
		}
	}
	//	for _, p := range portfolios {
	//		fmt.Println(p.ID, p.Name, p.PortfolioType, p.Limit, p.Parent)
	//	}
	return portfolios
}

func getChildren(portfolios []*Portfolio, pList []*Portfolio) []*Portfolio {
	pChildren := make([]*Portfolio, 0)
	if len(pList) == 0 {
		for _, p := range portfolios {
			if p.Parent == nil {
				pChildren = append(pChildren, p)
			}
		}
	} else {
		for _, p := range portfolios {
			for _, v := range pList {
				if p.Parent != nil && p.Parent.String() == v.ID.String() {
					pChildren = append(pChildren, p)
				}
			}
		}
	}
	return pChildren
}

type Node struct {
	portfolio *Portfolio
	children  []*Node
}

type Tree struct {
	root *Node
}

func (t *Tree) AddNode(p *Portfolio) {
	if p.Parent == nil {
		n := &Node{p, nil}
		t.root = n
	}
	else {
		n := &Node{p, nil}
	}
}

func processChildren(t *Tree, pChildren []*Portfolio) {
	for _, p := range pChildren {
		t.AddNode(p)
	}
}
func main() {
	fmt.Println("- start")
	portfolios := generate()
	tree := Tree{}
	fmt.Println(tree)
	pChildren := make([]*Portfolio, 0)
	pChildren = getChildren(portfolios, pChildren)
	for len(pChildren) > 0 {
		processChildren(&tree, pChildren)
		pChildren = getChildren(portfolios, pChildren)
	}
	fmt.Println(tree.root.portfolio)
}
