package main

import (
	"fmt"
)

type Portfolio struct {
	ID     int
	Name   string
	Parent *int
}

func NewPortfolio(id int, name string, parent *int) *Portfolio {
	return &Portfolio{ID: id, Name: name, Parent: parent}
}

type Node struct {
	portfolio *Portfolio
	children  []*Node
}

func (n *Node) AddNode(p *Portfolio) {
	if n.root == nil {
		node := &Node{portfolio: p}
		return node
	}

}

func main() {
	fmt.Println("- start")
	p_root := NewPortfolio(1, "default", nil)
	tree := &Node{portfolio: p_root}
	//	parent := 1
	//	p_it := NewPortfolio(2, "IT", &parent)
	//	tree.AddNode(p_it)
	//	p_hr := NewPortfolio(3, "HR", &parent)
	//	tree.AddNode(p_hr)
	//	p_sales := NewPortfolio(4, "Sales", &parent)
	//	tree.AddNode(p_sales)
	fmt.Println(tree)
}
