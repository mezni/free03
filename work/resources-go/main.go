package main

import (
	"fmt"
	"github.com/google/uuid"
	"github.com/mezni/resources-go/domain/entities"
)

type Tag struct {
	UUID uuid.UUID
	Type string
	Key  string
	Name string
}

type Resource struct {
	UUID uuid.UUID
	ID   string
	Name string
	Tags []*Tag
}

func main() {
	fmt.Println("- start")
	tag := entities.NewTag("cloud", "key", "value")
	fmt.Println(tag)
}
