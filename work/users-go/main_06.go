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
	uuid      uuid.UUID
	portfolio *Portfolio
	children  []*Node
}

type Tree struct {
	root *Node
}

func NewNode(portfolio *Portfolio) (*Node, error) {
	children := make([]*Node, 0)
	return &Node{uuid: portfolio.ID, portfolio: portfolio, children: children}, nil
}

func findAll(tree Tree) {
	queue := make([]*Node, 0)
	queue = append(queue, tree.root)
	for len(queue) > 0 {
		item := queue[0]
		fmt.Println(item.uuid, item.portfolio.Name)
		queue = queue[1:]
		if len(item.children) > 0 {
			for _, child := range item.children {
				queue = append(queue, child)
			}
		}
	}
}
func main() {
	fmt.Println("- start")
	tree := Tree{}
	p_root, _ := NewPortfolio("default", "root", 3000, nil)
	n_root, _ := NewNode(p_root)
	tree.root = n_root

	p_hr, _ := NewPortfolio("hr", "department", 1000, nil)
	n_hr, _ := NewNode(p_hr)

	p_it, _ := NewPortfolio("it", "department", 2000, nil)
	n_it, _ := NewNode(p_it)

	n_root.children = append(n_root.children, n_hr)
	n_root.children = append(n_root.children, n_it)

	p_phonix1, _ := NewPortfolio("phonix1", "projet", 500, nil)
	n_phonix1, _ := NewNode(p_phonix1)

	p_phonix2, _ := NewPortfolio("phonix2", "projet", 500, nil)
	n_phonix2, _ := NewNode(p_phonix2)

	n_it.children = append(n_it.children, n_phonix1)
	n_it.children = append(n_it.children, n_phonix2)

	findAll(tree)

}
