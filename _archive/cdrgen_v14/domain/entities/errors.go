package entities

import (
	"errors"
)

var (
	ErrMissingID     = errors.New("missing ID field in data")
	ErrInvalidID     = errors.New("invalid ID, must be a positive integer")
	ErrConverstionID = errors.New("invalid ID convertion")
	ErrEmptyName     = errors.New("name cannot be empty")
)
