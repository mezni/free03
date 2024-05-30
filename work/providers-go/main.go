package main

import (
	"fmt"
	"github.com/google/uuid"
)

type Provider struct {
	ProviderID  uuid.UUID
	Name        string
	Description string
	Regions     []Region
}

type Region struct {
	RegionID   uuid.UUID
	Name       string
	ProviderID uuid.UUID
}

func (p *Provider) AddRegion(region Region) {
	fmt.Printf("%s is assigning region %s\n", p.Name, region.Name)
}

func main() {
	fmt.Println("- start")
	provider := Provider{
		ProviderID:  uuid.New(),
		Name:        "AWS",
		Description: "AWS",
	}
	fmt.Println(provider)
	provider.AddRegion(Region{uuid.New(), "EAST1", provider.ProviderID})

}
