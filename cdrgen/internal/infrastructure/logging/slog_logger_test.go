package logger_test

import (
	"bytes"
	"context"
	"fmt"
	"strings"
	"sync"
	"testing"

	"github.com/mezni/wovoka/cdrgen/internal/infrastructure/logging"
)

func TestThreadSafeLogger(t *testing.T) {
	var buf bytes.Buffer
	l := logger.NewThreadSafeLogger(&buf, logger.DebugLevel) // Use your actual logger package and method

	ctx := context.WithValue(context.Background(), "module", "my_module")
	ctx = context.WithValue(ctx, "context", "my_context")

	// Test logging at different levels
	l.Debug(ctx, "This is a debug message")
	l.Info(ctx, "This is an info message")
	l.Warn(ctx, "This is a warn message")
	l.Error(ctx, "This is an error message")

	// Capture the output and check for expected log entries
	actual := buf.String()

	// Check if expected messages appear in the output (order may vary in concurrent tests)
	if !contains(actual, "DEBUG This is a debug message") {
		t.Errorf("Expected DEBUG log message not found: %s", actual)
	}
	if !contains(actual, "INFO This is an info message") {
		t.Errorf("Expected INFO log message not found: %s", actual)
	}
	if !contains(actual, "WARN This is a warn message") {
		t.Errorf("Expected WARN log message not found: %s", actual)
	}
	if !contains(actual, "ERROR This is an error message") {
		t.Errorf("Expected ERROR log message not found: %s", actual)
	}
}

// TestThreadSafeLoggerConcurrency tests logging in a concurrent environment.
func TestThreadSafeLoggerConcurrency(t *testing.T) {
	var buf bytes.Buffer
	l := logger.NewThreadSafeLogger(&buf, logger.DebugLevel) // Use your actual logger package and method

	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			ctx := context.WithValue(context.Background(), "module", fmt.Sprintf("module-%d", i))
			ctx = context.WithValue(ctx, "context", fmt.Sprintf("context-%d", i))
			l.Info(ctx, fmt.Sprintf("This is an info message from goroutine %d", i))
		}(i)
	}
	wg.Wait()

	// After concurrency, we check if the expected messages appear in the buffer.
	actual := buf.String()
	for i := 0; i < 10; i++ {
		expectedMessage := fmt.Sprintf("INFO This is an info message from goroutine %d", i)
		if !contains(actual, expectedMessage) {
			t.Errorf("Expected log message not found: %s", expectedMessage)
		}
	}
}

// TestThreadSafeLoggerSetLevel tests changing log levels.
func TestThreadSafeLoggerSetLevel(t *testing.T) {
	var buf bytes.Buffer
	l := logger.NewThreadSafeLogger(&buf, logger.DebugLevel) // Use your actual logger package and method

	// Change the level to InfoLevel
	l.SetLevel(logger.InfoLevel)
	if l.GetLevel() != logger.InfoLevel {
		t.Errorf("Expected log level to be %d, but got %d", logger.InfoLevel, l.GetLevel())
	}
}

// TestThreadSafeLoggerGetLevel tests getting the current log level.
func TestThreadSafeLoggerGetLevel(t *testing.T) {
	var buf bytes.Buffer
	l := logger.NewThreadSafeLogger(&buf, logger.DebugLevel) // Use your actual logger package and method

	// Check if the initial log level is DebugLevel
	if l.GetLevel() != logger.DebugLevel {
		t.Errorf("Expected log level to be %d, but got %d", logger.DebugLevel, l.GetLevel())
	}
}

// Helper function to check if a substring exists in the log output
func contains(logOutput, substr string) bool {
	return strings.Contains(logOutput, substr)
}
