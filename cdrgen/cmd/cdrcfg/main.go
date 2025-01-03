package main

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/application/interfaces"
	"log"
)

func main() {
	// JSON data

	// Initialize a variable to store the unmarshalled data
	var config interfaces.Config

	config, err := interfaces.ReadConfig()

	if err != nil {
		log.Fatalf("Error unmarshalling JSON: %v", err)
	}

	// Print the unmarshalled configuration
	fmt.Println("Network Technologies:")
	for _, nt := range config.NetworkTechnologies {
		fmt.Printf("- %s: %s\n", nt.Name, nt.Description)
	}

	fmt.Println("\nNetwork Element Types:")
	for _, netType := range config.NetworkElementTypes {
		fmt.Printf("- %s: %s (Technology: %s)\n", netType.Name, netType.Description, netType.NetworkTechnology)
	}

	fmt.Println("\nService Types:")
	for _, service := range config.ServiceTypes {
		fmt.Printf("- %s: %s (Technology: %s)\n", service.Name, service.Description, service.NetworkTechnology)
	}

	fmt.Println("\nService Nodes:")
	for _, node := range config.ServiceNodes {
		fmt.Printf("- %s (Technology: %s)\n", node.Name, node.NetworkTechnology)
	}
}
