// logger.go

package logger

import (
	"context"
)

// LogLevel represents the level of logging
type LogLevel uint8

const (
	// DebugLevel is for debug messages
	DebugLevel LogLevel = iota
	// InfoLevel is for info messages
	InfoLevel
	// WarnLevel is for warn messages
	WarnLevel
	// ErrorLevel is for error messages
	ErrorLevel
)

// Logger is the interface for logging
type Logger interface {
	// Debug logs a debug message
	Debug(ctx context.Context, msg string)
	// Info logs an info message
	Info(ctx context.Context, msg string)
	// Warn logs a warn message
	Warn(ctx context.Context, msg string)
	// Error logs an error message
	Error(ctx context.Context, msg string)
	// SetLevel sets the logging level
	SetLevel(level LogLevel)
	// GetLevel gets the current logging level
	GetLevel() LogLevel
}
