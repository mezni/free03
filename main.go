package main

import (
	"fmt"
	"log"
	"time"

	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
)

func main() {
	// Initialize the database manager
	manager, err := boltstore.NewBoltDBManager("data.db", 5*time.Second)
	if err != nil {
		log.Fatal("Failed to initialize BoltDB:", err)
	}
	defer manager.Close()

	// Initialize the example repository
	configRepo := boltstore.NewConfigRepository(manager)

	// Define the NetworkTechnology type
	type NetworkTechnology struct {
		ID   string
		Name string
		Description string
	}

	// Save multiple items in one transaction to "NetworkTechnologies"
	items := map[string]interface{}{
		"2G": NetworkTechnology{ID: "2G", Name: "2G", Description: "GSM (Global System for Mobile Communications), CDMA (Code Division Multiple Access)"},
		"3G": NetworkTechnology{ID: "3G", Name: "3G", Description: "UMTS (Universal Mobile Telecommunications System), CDMA2000"},
		"4G": NetworkTechnology{ID: "4G", Name: "4G", Description: "LTE (Long-Term Evolution)"},
		"5G": NetworkTechnology{ID: "5G", Name: "5G", Description: "5G NR (New Radio)"},
	}

	if err := configRepo.SaveMany("NetworkTechnologies", items); err != nil {
		log.Fatal("Failed to save many data:", err)
	}

	// Retrieve all data from "NetworkTechnologies"
	var allData []NetworkTechnology
	if err := configRepo.GetAll("NetworkTechnologies", &allData); err != nil {
		log.Fatal("Failed to retrieve all data from NetworkTechnologies:", err)
	}

	// Print all retrieved data
	fmt.Println("All data in NetworkTechnologies:")
	for _, data := range allData {
		fmt.Printf("ID: %s, Name: %s, Desc: %s\n", data.ID, data.Name, data.Description)
	}
}
