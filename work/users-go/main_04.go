package main

import (
	"fmt"
	"github.com/google/uuid"
)

// TreeNode represents a node in the tree
type TreeNode struct {
	Id       uuid.UUID
	Children []*TreeNode
}

type Tree struct {
	Root *TreeNode
}

func (t *Tree) Insert(id uuid.UUID) {
	t.Root = &TreeNode{id, nil}
}

func main() {
	t := Tree{}
	fmt.Println(t)
	t.Insert(uuid.New())
	fmt.Println(t)
}
