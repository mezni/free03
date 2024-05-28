package main

import (
	"fmt"
	"github.com/google/uuid"
)

type Node struct {
	id       uuid.UUID
	children []*Node
}

type Tree struct {
	root *Node
}

func (t *Tree) AddNode() {
	n := &Node{uuid.New(), nil}
	if t.root == nil {
		t.root = n
	}
}

func main() {
	fmt.Println("- start")
	tree := Tree{}
	tree.AddNode()
	fmt.Println(tree)
}
