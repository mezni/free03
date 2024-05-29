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

type PortfolioNode struct {
	uuid      uuid.UUID
	portfolio *Portfolio
	children  []*PortfolioNode
}

type PortfolioTree struct {
	root *PortfolioNode
}

func NewPortfolio(name string, portfolioType string, limit float64, parent *uuid.UUID) (*Portfolio, error) {
	return &Portfolio{ID: uuid.New(), Name: name, PortfolioType: portfolioType, Limit: limit, Parent: parent}, nil
}

func NewNode(p *Portfolio) (*PortfolioNode, error) {
	children := make([]*PortfolioNode, 0)
	return &PortfolioNode{uuid: p.ID, portfolio: p, children: children}, nil
}

func (t *PortfolioTree) AddNode(p *Portfolio) (*PortfolioNode, error) {
	if t.root == nil {
		if p.Parent == nil {
			node, _ := NewNode(p)
			t.root = node
			return node, nil
		}
	}
	return nil, nil

}

//func (t *PortfolioTree) GetParent(p *Portfolio) (*PortfolioNode, error) {
//	queue := make([]*PortfolioNode, 0)
//	queue = append(queue, t.root)
//	for len(queue) > 0 {
//		item := queue[0]
//		queue = queue[1:]
//	}
//	return nil, nil
//}

func main() {
	fmt.Println("- start")
	tree := PortfolioTree{}
	//	p_root, _ := NewPortfolio("default", "root", 3000, nil)
	//	x, y := tree.GetParent(p_root)
	//	fmt.Println(x, y)
	//	n_root, _ := tree.AddNode(p_root)
	//	fmt.Println(n_root)
	fmt.Println(tree)
}
