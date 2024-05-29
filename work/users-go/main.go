package main

import (
	"errors"
	"fmt"
	"github.com/google/uuid"
)

var (
	ErrCantAddRoot    = errors.New("cant add root node to tree")
	ErrTreeHasNoRoot  = errors.New("cant add no root node to empty tree")
	ErrParentNotFound = errors.New("parent not found")
)

type Portfolio struct {
	ID            uuid.UUID
	Name          string
	PortfolioType string
	Limit         float64
	Parent        uuid.UUID
}

func NewPortfolio(name string, portfolioType string, limit float64, parent uuid.UUID) (*Portfolio, error) {
	return &Portfolio{ID: uuid.New(), Name: name, PortfolioType: portfolioType, Limit: limit, Parent: parent}, nil
}

type PortfolioNode struct {
	uuid      uuid.UUID
	portfolio *Portfolio
	children  []*PortfolioNode
}

type PortfolioTree struct {
	root *PortfolioNode
}

func NewNode(p *Portfolio) (*PortfolioNode, error) {
	children := make([]*PortfolioNode, 0)
	return &PortfolioNode{uuid: p.ID, portfolio: p, children: children}, nil
}

func (t *PortfolioTree) AddNodeByUUID(u uuid.UUID) *PortfolioNode {
	if t.root == nil {
		return nil
	} else {
		queue := make([]*PortfolioNode, 0)
		queue = append(queue, t.root)
		for len(queue) > 0 {
			item := queue[0]
			if item.uuid == u {
				return item
			} else {
				queue = queue[1:]
				if len(item.children) > 0 {
					for _, child := range item.children {
						queue = append(queue, child)
					}
				}
			}
		}
	}
	return nil
}

func (t *PortfolioTree) AddNode(p *Portfolio) (*PortfolioNode, error) {
	if p.Parent == uuid.Nil {
		if t.root == nil {
			node, _ := NewNode(p)
			t.root = node
			return node, nil
		} else {
			return nil, ErrCantAddRoot
		}
	} else {
		parent := t.AddNodeByUUID(p.Parent)
		if parent == nil {
			return nil, ErrParentNotFound
		} else {
			node, _ := NewNode(p)
			parent.children = append(parent.children, node)
			return node, nil
		}
	}

}

func (t *PortfolioTree) PrintTree() {
	if t.root == nil {
		fmt.Println("Empty Tree")
	} else {
		queue := make([]*PortfolioNode, 0)
		queue = append(queue, t.root)
		for len(queue) > 0 {
			item := queue[0]
			queue = queue[1:]
			fmt.Println("Node: ", item.portfolio.Name, item.portfolio.Limit)
			if len(item.children) > 0 {
				for _, child := range item.children {
					queue = append(queue, child)
					fmt.Println("- Child: ", child.portfolio.Name, child.portfolio.Limit)
				}
			}
		}
	}

}

func main() {
	fmt.Println("- start")
	fmt.Println("- load")
	tree := PortfolioTree{}
	p_root, _ := NewPortfolio("default", "root", 4000, uuid.Nil)
	p_it, _ := NewPortfolio("it", "department", 2000, p_root.ID)
	p_hr, _ := NewPortfolio("hr", "department", 1000, p_root.ID)
	p_sales, _ := NewPortfolio("sales", "department", 1000, p_root.ID)
	p_phonix1, _ := NewPortfolio("phonix1", "project", 500, p_it.ID)
	p_phonix2, _ := NewPortfolio("phonix2", "project", 500, p_it.ID)

	portfolios := []*Portfolio{p_root, p_it, p_hr, p_sales, p_phonix1, p_phonix2}
	for _, p := range portfolios {
		_, _ = tree.AddNode(p)
	}
	fmt.Println("- process")
	tree.PrintTree()
	fmt.Println(tree)

}
