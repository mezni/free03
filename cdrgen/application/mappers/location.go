package mappers

import (
	"errors"

	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

type BaselineMapper struct{}

// ToNetworkTechnologies maps a slice of NetworkTechnologyDTO to NetworkTechnology entities
func (b *BaselineMapper) ToNetworkTechnologies(networkTechnologies []dtos.NetworkTechnologyDTO) ([]entities.NetworkTechnology, error) {
	if len(networkTechnologies) == 0 {
		return nil, errors.New("network technologies list is empty")
	}

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

// ToNetworkElementTypes maps a slice of NetworkElementTypeDTO to NetworkElementType entities
func (b *BaselineMapper) ToNetworkElementTypes(networkElementTypes []dtos.NetworkElementTypeDTO) ([]entities.NetworkElementType, error) {
	if len(networkElementTypes) == 0 {
		return nil, errors.New("network element types list is empty")
	}

	var networkElementTypeList []entities.NetworkElementType
	idseq := 1

	for _, ne := range networkElementTypes {
		neInstance := entities.NetworkElementType{
			ID:                idseq,
			Name:              ne.Name,
			Description:       ne.Description,
			NetworkTechnology: ne.NetworkTechnology,
		}
		networkElementTypeList = append(networkElementTypeList, neInstance)
		idseq++
	}

	return networkElementTypeList, nil
}

// ToServiceTypes maps a slice of ServiceTypeDTO to ServiceType entities
func (b *BaselineMapper) ToServiceTypes(serviceTypes []dtos.ServiceTypeDTO) ([]entities.ServiceType, error) {
	if len(serviceTypes) == 0 {
		return nil, errors.New("service types list is empty")
	}

	var serviceTypeList []entities.ServiceType
	idseq := 1

	for _, st := range serviceTypes {
		stInstance := entities.ServiceType{
			ID:                idseq,
			Name:              st.Name,
			Description:       st.Description,
			NetworkTechnology: st.NetworkTechnology,
		}
		serviceTypeList = append(serviceTypeList, stInstance)
		idseq++
	}

	return serviceTypeList, nil
}