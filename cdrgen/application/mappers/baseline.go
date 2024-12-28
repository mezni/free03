package services

import (
	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

type BaselineMapper struct{}

func (b *BaselineMapper) ToNetworkTechnologies(networkTechnologies []dtos.NetworkTechnologyDTO) ([]entities.NetworkTechnology, error) {
	var networkTechnologyList []entities.NetworkTechnology
	idseq := 1

	for _, nt := range networkTechnologies {
		ntInstance := entities.NetworkTechnology{
			ID:          idseq,
			Name:        nt.Name,
			Description: nt.Description,
		}
		networkTechnologyList = append(networkTechnologyList, ntInstance)
		idseq++
	}

	return networkTechnologyList, nil
}
