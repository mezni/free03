package errors

import "errors"

// Common error messages
var (
	ErrInvalidID           = errors.New("ID must be greater than 0")
	ErrEmptyName           = errors.New("Name cannot be empty")
	ErrEmptyTechName       = errors.New("NetworkTechnologyName cannot be empty")
)
