package main

import (
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/application/services"
)

func main() {
	// Initialize the loader service
	loaderService, err := services.NewLoaderService("cdrgen.db")
	if err != nil {
		log.Fatalf("Error initializing loader service: %v", err)
	}
	defer loaderService.Close()

	// Step 1: Retrieve all network technologies from the database
	networkTechnologies, err := loaderService.NetworkTechRepo.GetAll()
	if err != nil {
		log.Fatalf("Error retrieving network technologies: %v", err)
	}

	// Step 2: Print the retrieved network technologies
	fmt.Println("All Network Technologies in Database:")
	for _, nt := range networkTechnologies {
		fmt.Printf("ID: %d, Name: %s, Description: %s\n", nt.ID, nt.Name, nt.Description)
	}

	// Step 3: Retrieve all network element types from the database
	networkElementTypes, err := loaderService.NetworkElementTypeRepo.GetAll()
	if err != nil {
		log.Fatalf("Error retrieving network element types: %v", err)
	}

	// Step 4: Print the retrieved network element types
	fmt.Println("\nAll Network Element Types in Database:")
	for _, net := range networkElementTypes {
		fmt.Printf("ID: %d, Name: %s, Description: %s, Network Technology: %s\n",
			net.ID, net.Name, net.Description, net.NetworkTechnology)
	}

	// Step 5: Retrieve all service types from the database
	serviceTypes, err := loaderService.ServiceTypeRepo.GetAll()
	if err != nil {
		log.Fatalf("Error retrieving service types: %v", err)
	}

	// Step 6: Print the retrieved service types
	fmt.Println("\nAll Service Types in Database:")
	for _, st := range serviceTypes {
		fmt.Printf("ID: %d, Name: %s, Description: %s, Network Technology: %s, Bearer Type: %s, Jitter Min: %d\n",
			st.ID, st.Name, st.Description, st.NetworkTechnology, st.BearerType, st.JitterMin)
	}

	// Step 7: Retrieve all service nodes from the database
	serviceNodes, err := loaderService.ServiceNodeRepo.GetAll()
	if err != nil {
		log.Fatalf("Error retrieving service nodes: %v", err)
	}

	// Step 8: Print the retrieved service nodes
	fmt.Println("\nAll Service Nodes in Database:")
	for _, sn := range serviceNodes {
		fmt.Printf("ID: %d, Name: %s, Service Name: %s, Network Technology: %s\n",
			sn.ID, sn.Name, sn.ServiceName, sn.NetworkTechnology)
	}

	// Step 9: Retrieve all locations from the database
	locations, err := loaderService.LocationRepo.GetAll()
	if err != nil {
		log.Fatalf("Error retrieving locations: %v", err)
	}

	// Step 10: Print the retrieved locations
	fmt.Println("\nAll Locations in Database:")
	for _, loc := range locations {
		fmt.Printf("ID: %d, Name: %s, LatitudeMin: %f, LatitudeMax: %f, LongitudeMin: %f, LongitudeMax: %f, AreaCode: %s, NetworkTechnology: %s\n",
			loc.ID, loc.Name, loc.LatitudeMin, loc.LatitudeMax, loc.LongitudeMin, loc.LongitudeMax, loc.AreaCode, loc.NetworkTechnology)
	}
}
