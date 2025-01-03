package main

import (
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
}
