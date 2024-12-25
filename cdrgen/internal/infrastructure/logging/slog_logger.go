package logger

import (
	"context"
	"fmt"
	"io"
	"log"
	"sync"
	"time"
)

// SimpleLogger is a thread-safe implementation of the Logger interface
type SimpleLogger struct {
	mu    sync.Mutex
	out   *log.Logger
	level LogLevel
}

// NewSimpleLogger returns a new SimpleLogger instance
func NewSimpleLogger(out io.Writer, level LogLevel) *SimpleLogger {
	return &SimpleLogger{
		out:   log.New(out, "", 0),
		level: level,
	}
}

// Debug logs a debug message
func (l *SimpleLogger) Debug(ctx context.Context, msg string) {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.level <= DebugLevel {
		l.out.Println(formatLogMessage(ctx, DebugLevel, msg))
	}
}

// Info logs an info message
func (l *SimpleLogger) Info(ctx context.Context, msg string) {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.level <= InfoLevel {
		l.out.Println(formatLogMessage(ctx, InfoLevel, msg))
	}
}

// Warn logs a warn message
func (l *SimpleLogger) Warn(ctx context.Context, msg string) {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.level <= WarnLevel {
		l.out.Println(formatLogMessage(ctx, WarnLevel, msg))
	}
}

// Error logs an error message
func (l *SimpleLogger) Error(ctx context.Context, msg string) {
	l.mu.Lock()
	defer l.mu.Unlock()
	if l.level <= ErrorLevel {
		l.out.Println(formatLogMessage(ctx, ErrorLevel, msg))
	}
}

// SetLevel sets the logging level
func (l *SimpleLogger) SetLevel(level LogLevel) {
	l.mu.Lock()
	defer l.mu.Unlock()
	l.level = level
}

// GetLevel gets the current logging level
func (l *SimpleLogger) GetLevel() LogLevel {
	l.mu.Lock()
	defer l.mu.Unlock()
	return l.level
}

// formatLogMessage formats the log message with timestamp, level, and context
func formatLogMessage(ctx context.Context, level LogLevel, msg string) string {
	now := time.Now().Format(time.RFC3339Nano) // Timestamp in RFC3339Nano format
//	now = now[:23]
	levelStr := getLevelString(level)
	module := getModule(ctx)      // Get the "module" value from context
	contextStr := getContext(ctx) // Get other context values (optional)

	// Build the log message
	return fmt.Sprintf("[%s] [%s] [%s] %s - %s", now, module, levelStr, msg, contextStr)
}

// getLevelString converts a LogLevel to its corresponding string representation
func getLevelString(level LogLevel) string {
	switch level {
	case DebugLevel:
		return "DEBUG"
	case InfoLevel:
		return "INFO"
	case WarnLevel:
		return "WARN"
	case ErrorLevel:
		return "ERROR"
	default:
		return "UNKNOWN"
	}
}

// getModule retrieves the "module" value from the context if available
func getModule(ctx context.Context) string {
	module, ok := ctx.Value("module").(string)
	if !ok {
		return "unknown" // Default to "unknown" if the "module" key is not found
	}
	return module
}

// getContext retrieves the "context" value from the context if available
func getContext(ctx context.Context) string {
	contextStr, ok := ctx.Value("context").(string)
	if !ok {
		return "" // Default to empty if the "context" key is not found
	}
	return contextStr
}
