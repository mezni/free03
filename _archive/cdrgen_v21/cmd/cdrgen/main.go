package main

import (
		"encoding/json"
	"database/sql"
	"fmt"
	"log"

	_ "github.com/mattn/go-sqlite3"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

func main() {
	// Open the SQLite database
	db, err := sql.Open("sqlite3", "./baseline.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	// Query to fetch all records from the 'network_technologies' table
	rows, err := db.Query("SELECT id, name, description FROM network_technologies")
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()

	// Initialize a slice to hold the network technologies
	var networkTechnologies []entities.NetworkTechnology

	// Iterate through the rows and scan the results into the slice
	for rows.Next() {
		var nt entities.NetworkTechnology
		// Scan the columns into the NetworkTechnology struct
		if err := rows.Scan(&nt.ID, &nt.Name, &nt.Description); err != nil {
			log.Fatal(err)
		}
		// Append the scanned network technology to the slice
		networkTechnologies = append(networkTechnologies, nt)
	}

	// Check for any error that might have occurred while iterating over rows
	if err := rows.Err(); err != nil {
		log.Fatal(err)
	}

	// Output the network technologies
	for _, nt := range networkTechnologies {
		fmt.Printf("Network Technology ID: %d, Name: %s, Description: %s\n", nt.ID, nt.Name, nt.Description)
	}

	// Fetch and print the network element types
	networkElementRows, err := db.Query("SELECT id, name, description, network_technology FROM network_element_types")
	if err != nil {
		log.Fatal(err)
	}
	defer networkElementRows.Close()

	// Initialize a slice to hold the network element types
	var networkElementTypes []entities.NetworkElementType

	// Iterate through the network element type rows and scan the results into the slice
	for networkElementRows.Next() {
		var netElement entities.NetworkElementType
		// Scan the columns into the NetworkElementType struct
		if err := networkElementRows.Scan(&netElement.ID, &netElement.Name, &netElement.Description, &netElement.NetworkTechnology); err != nil {
			log.Fatal(err)
		}
		// Append the scanned network element type to the slice
		networkElementTypes = append(networkElementTypes, netElement)
	}

	// Check for any error that might have occurred while iterating over rows
	if err := networkElementRows.Err(); err != nil {
		log.Fatal(err)
	}

	// Output the network element types
	for _, netElement := range networkElementTypes {
		fmt.Printf("Network Element Type ID: %d, Name: %s, Description: %s, Network Technology: %s\n", netElement.ID, netElement.Name, netElement.Description, netElement.NetworkTechnology)
	}

	// Now fetch and print the locations
	locationRows, err := db.Query("SELECT id, network_technology, name, latitude_min, latitude_max, longitude_min, longitude_max, area_code FROM locations")
	if err != nil {
		log.Fatal(err)
	}
	defer locationRows.Close()

	// Initialize a slice to hold the locations
	var locations []entities.Location

	// Iterate through the location rows and scan the results into the slice
	for locationRows.Next() {
		var location entities.Location
		// Scan the columns into the Location struct
		if err := locationRows.Scan(
			&location.ID,
			&location.NetworkTechnology,
			&location.Name,
			&location.LatitudeMin,
			&location.LatitudeMax,
			&location.LongitudeMin,
			&location.LongitudeMax,
			&location.AreaCode,
		); err != nil {
			log.Fatal(err)
		}
		// Append the scanned location to the slice
		locations = append(locations, location)
	}

	// Check for any error that might have occurred while iterating over rows
	if err := locationRows.Err(); err != nil {
		log.Fatal(err)
	}

	// Output the locations
	for _, location := range locations {
		fmt.Printf("Location ID: %d, Network Technology: %s, Name: %s, Latitude Min: %f, Latitude Max: %f, Longitude Min: %f, Longitude Max: %f, Area Code: %s\n",
			location.ID, location.NetworkTechnology, location.Name,
			location.LatitudeMin, location.LatitudeMax,
			location.LongitudeMin, location.LongitudeMax,
			location.AreaCode)
	}

	// Fetch and print the service types
	serviceTypeRows, err := db.Query("SELECT id, name, description, network_technology, nodes, bearer_type, jitter_min, jitter_max, latency_min, latency_max, throughput_min, throughput_max, packet_loss_min, packet_loss_max, call_setup_time_min, call_setup_time_max, mos_range_min, mos_range_max FROM service_types")
	if err != nil {
		log.Fatal(err)
	}
	defer serviceTypeRows.Close()

	// Initialize a slice to hold the service types
	var serviceTypes []entities.ServiceType

	// Iterate through the rows and scan the results into the slice
	for rows.Next() {
		var serviceType entities.ServiceType

		// Scan the columns into the ServiceType struct
		var nodesJSON string
		if err := rows.Scan(
			&serviceType.ID,
			&serviceType.Name,
			&serviceType.Description,
			&serviceType.NetworkTechnology,
			&nodesJSON,  // Scan nodes as a string
			&serviceType.BearerType,
			&serviceType.JitterMin,
			&serviceType.JitterMax,
			&serviceType.LatencyMin,
			&serviceType.LatencyMax,
			&serviceType.ThroughputMin,
			&serviceType.ThroughputMax,
			&serviceType.PacketLossMin,
			&serviceType.PacketLossMax,
			&serviceType.CallSetupTimeMin,
			&serviceType.CallSetupTimeMax,
			&serviceType.MosRangeMin,
			&serviceType.MosRangeMax,
		); err != nil {
			log.Fatal(err)
		}

		// Unmarshal the JSON string into a []string slice for the nodes
		if err := json.Unmarshal([]byte(nodesJSON), &serviceType.Nodes); err != nil {
			log.Fatal(err)
		}

		// Append the scanned service type to the slice
		serviceTypes = append(serviceTypes, serviceType)
	}

	// Check for any error that might have occurred while iterating over rows
	if err := rows.Err(); err != nil {
		log.Fatal(err)
	}

	// Output the service types
	for _, serviceType := range serviceTypes {
		fmt.Printf("ServiceType ID: %d, Name: %s, Description: %s, Network Technology: %s, Nodes: %v, BearerType: %s, Jitter Min: %d, Jitter Max: %d, Latency Min: %d, Latency Max: %d, Throughput Min: %d, Throughput Max: %d, Packet Loss Min: %d, Packet Loss Max: %d, Call Setup Time Min: %d, Call Setup Time Max: %d, MOS Min: %f, MOS Max: %f\n",
			serviceType.ID, serviceType.Name, serviceType.Description, serviceType.NetworkTechnology,
			serviceType.Nodes, serviceType.BearerType, serviceType.JitterMin, serviceType.JitterMax,
			serviceType.LatencyMin, serviceType.LatencyMax, serviceType.ThroughputMin, serviceType.ThroughputMax,
			serviceType.PacketLossMin, serviceType.PacketLossMax, serviceType.CallSetupTimeMin,
			serviceType.CallSetupTimeMax, serviceType.MosRangeMin, serviceType.MosRangeMax)
	}
}
