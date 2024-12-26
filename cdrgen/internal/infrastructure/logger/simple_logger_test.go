package logger_test

import (
	"context"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/internal/infrastructure/logger"
	"io/ioutil"
	"sync"
	"testing"
)

func TestSimpleLogger(t *testing.T) {
	out := ioutil.Discard
	l := logger.NewSimpleLogger(out, logger.DebugLevel)

	ctx := context.WithValue(context.Background(), "module", "my_module")
	ctx = context.WithValue(ctx, "context", "my_context")

	l.Debug(ctx, "This is a debug message")
	l.Info(ctx, "This is an info message")
	l.Warn(ctx, "This is a warn message")
	l.Error(ctx, "This is an error message")
}

func TestSimpleLoggerConcurrency(t *testing.T) {
	out := ioutil.Discard
	l := logger.NewSimpleLogger(out, logger.DebugLevel)

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
}

func TestSimpleLoggerSetLevel(t *testing.T) {
	out := ioutil.Discard
	l := logger.NewSimpleLogger(out, logger.DebugLevel)

	l.SetLevel(logger.InfoLevel)
	if l.GetLevel() != logger.InfoLevel {
		t.Errorf("Expected log level to be %d, but got %d", logger.InfoLevel, l.GetLevel())
	}
}

func TestSimpleLoggerGetLevel(t *testing.T) {
	out := ioutil.Discard
	l := logger.NewSimpleLogger(out, logger.DebugLevel)

	if l.GetLevel() != logger.DebugLevel {
		t.Errorf("Expected log level to be %d, but got %d", logger.DebugLevel, l.GetLevel())
	}
}
