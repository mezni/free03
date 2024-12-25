package main

import (
	"flag"
	"fmt"
	"log"
	"os"
)

// Version will be set during build time using -ldflags
var version = "development" // default version

func main() {
	// Define flags
	configFile := flag.String("f", "", "Path to the config file (required)")
	databaseName := flag.String("d", "", "Name of the BoltDB database (required)")
	showVersion := flag.Bool("v", false, "Show the version of the tool")
	showHelp := flag.Bool("h", false, "Show help information")

	// Customize flag usage
	flag.Usage = func() {
		fmt.Fprintf(flag.CommandLine.Output(), "Usage of %s:\n", os.Args[0])
		flag.PrintDefaults()
	}

	// Parse flags
	flag.Parse()

	// Handle help flag
	if *showHelp {
		flag.Usage()
		os.Exit(0)
	}

	// Handle version flag
	if *showVersion {
		fmt.Printf("%s version %s\n", os.Args[0], version)
		os.Exit(0)
	}

	// Validate required flags
	if *configFile == "" || *databaseName == "" {
		fmt.Fprintln(os.Stderr, "Error: Both -f (config file) and -d (database name) are required.")
		flag.Usage()
		os.Exit(1)
	}

	// Validate config file existence
	if _, err := os.Stat(*configFile); os.IsNotExist(err) {
		log.Fatalf("Error: Config file '%s' does not exist.\n", *configFile)
	}

	// Proceed with application logic
	fmt.Printf("Successfully verified the config file '%s' and opened the database '%s'.\n", *configFile, *databaseName)
}
