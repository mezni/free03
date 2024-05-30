package entities

import (
	"github.com/google/uuid"
)

type Tag struct {
	UUID uuid.UUID
	Type string
	Key  string
	Name string
}

func NewTag(tagType string, key string, name string) *Tag {
	return &Tag{
		UUID: uuid.New(),
		Type: tagType,
		Key:  key,
		Name: name,
	}
}
