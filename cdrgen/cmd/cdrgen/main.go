package main

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/application/services"
)

func main() {
	// Initialize repositories
	memoryRepo := repositories.NewMemoryCDRRepository()
	customerRepo := repositories.NewMemoryCustomerRepository()
	networkElementRepo := repositories.NewMemoryNetworkElementRepository()

	// Add sample customers
	customerRepo.AddCustomer(domain.Customer{ID: "1", MSISDN: "12345", IMSI: "imsi1", IMEI: "imei1"})
	customerRepo.AddCustomer(domain.Customer{ID: "2", MSISDN: "67890", IMSI: "imsi2", IMEI: "imei2"})
	customerRepo.AddCustomer(domain.Customer{ID: "3", MSISDN: "11223", IMSI: "imsi3", IMEI: "imei3"})

	// Add sample network elements
	networkElementRepo.AddNetworkElement(domain.NetworkElement{ID: "NE1", Name: "BTS01", Location: "New York", Type: "BTS"})
	networkElementRepo.AddNetworkElement(domain.NetworkElement{ID: "NE2", Name: "MSC01", Location: "Chicago", Type: "MSC"})
	networkElementRepo.AddNetworkElement(domain.NetworkElement{ID: "NE3", Name: "Router01", Location: "Dallas", Type: "Router"})

	// Initialize CDR service
	service := application.NewCDRService([]domain.CDRRepository{memoryRepo}, customerRepo, networkElementRepo)

	// Generate a random CDR
	cdr, err := service.GenerateRandomCDR("outgoing", 300)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println("Generated CDR:", cdr)

	// Fetch all CDRs
	cdrs, err := memoryRepo.FindAll()
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println("All CDRs:", cdrs)
}
