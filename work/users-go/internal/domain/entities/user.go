package entities

import (
	"errors"
	"github.com/google/uuid"
	"time"
)

type User struct {
	ID        uuid.UUID
	Name      string
	CreatedAt time.Time
	UpdatedAt time.Time
}

func (u *User) validate() error {
	if u.Name == "" {
		return errors.New("name must not be empty")
	}
	return nil
}

func NewUser(name string) *User {
	return &User{
		ID:        uuid.New(),
		Name:      name,
		CreatedAt: time.Now(),
		UpdatedAt: time.Time{},
	}
}

func (u *User) UpdateName(name string) error {
	if u.Name != name {
		u.Name = name
		u.UpdatedAt = time.Now()

		return u.validate()
	}
	return nil
}
