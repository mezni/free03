package main

import (
	"context"

	"os"
	"github.com/mezni/wovoka/cdrgen/internal/infrastructure/logging"
)

func main() {
	l := logger.NewSimpleLogger(os.Stdout, logger.DebugLevel)
	ctx := context.WithValue(context.Background(), "module", "cdrgen")
	ctx = context.WithValue(ctx, "context", "request_123")
	l.Info(ctx, "Startup")
	l.Info(ctx, "Shutdown")
}
