package services

import (
	"fmt"

	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"encoding/json"
	"io"
	"os"
)

// BaselineService provides methods to work with the entities
type BaselineService struct {
	FilePath string
}

// NewBaselineService creates a new service with the given file path
func NewBaselineService(filePath string) *BaselineService {
	return &BaselineService{FilePath: filePath}
}

// ReadData reads the JSON file and returns the network technologies, element types, and service types as DTOs.
func (s *BaselineService) ReadData() (*dtos.BaselineData, error) {
	// Read the file using the helper function
	data, err := ReadFile(s.FilePath)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %w", err)
	}

	// Unmarshal JSON into a BaselineData DTO
	var result dtos.BaselineData
	if err := json.Unmarshal(data, &result); err != nil {
		return nil, fmt.Errorf("failed to unmarshal JSON: %w", err)
	}

	return &result, nil
}

// AssignID is a helper function to assign an ID to any entity that has an ID field.
func AssignID(entity any, id int) {
	switch e := entity.(type) {
	case *entities.NetworkTechnology:
		e.ID = id
	case *entities.NetworkElementType:
		e.ID = id
	case *entities.ServiceType:
		e.ID = id
	default:
		fmt.Printf("Entity of type %T does not have an ID field to assign.\n", e)
	}
}

// MapToEntities is a generic function to map any DTO list to a corresponding entity list.
func MapToEntities[DTO, Entity any](dtoList []DTO, mapFunc func(DTO) Entity) []Entity {
	var entityList []Entity

	for i, dto := range dtoList {
		entity := mapFunc(dto) // Apply the mapping function to each DTO
		// Assign the ID to the entity starting from 1
		AssignID(&entity, i+1)
		entityList = append(entityList, entity)
	}

	return entityList
}

// MapNetworkTechnologyDTOToEntity maps a NetworkTechnologyDTO to a NetworkTechnology entity.
func MapNetworkTechnologyDTOToEntity(ntDTO dtos.NetworkTechnologyDTO) entities.NetworkTechnology {
	return entities.NetworkTechnology{
		Name:        ntDTO.Name,
		Description: ntDTO.Description,
	}
}

// MapNetworkElementTypeDTOToEntity maps a NetworkElementTypeDTO to a NetworkElementType entity.
func MapNetworkElementTypeDTOToEntity(netElemDTO dtos.NetworkElementTypeDTO) entities.NetworkElementType {
	return entities.NetworkElementType{
		Name:              netElemDTO.Name,
		Description:       netElemDTO.Description,
		NetworkTechnology: netElemDTO.NetworkTechnology,
	}
}

// MapServiceTypeDTOToEntity maps a ServiceTypeDTO to a ServiceType entity.
func MapServiceTypeDTOToEntity(serviceDTO dtos.ServiceTypeDTO) entities.ServiceType {
	return entities.ServiceType{
		Name:              serviceDTO.Name,
		Description:       serviceDTO.Description,
		NetworkTechnology: serviceDTO.NetworkTechnology,
	}
}

// ReadFile reads the content of the given file path and returns it as a byte slice
func ReadFile(filePath string) ([]byte, error) {
	// Open the file
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	// Read file contents
	data, err := io.ReadAll(file)
	if err != nil {
		return nil, fmt.Errorf("failed to read file: %w", err)
	}

	return data, nil
}

// MapFileDataToEntities converts the file data into entities
func (s *BaselineService) MapFileDataToEntities() ([]entities.NetworkTechnology, []entities.NetworkElementType, []entities.ServiceType, error) {
	// Read and unmarshal the data into DTOs
	data, err := s.ReadData()
	if err != nil {
		return nil, nil, nil, fmt.Errorf("failed to read data: %w", err)
	}

	// Convert NetworkTechnologies DTOs to entities
	networkTechnologies := MapToEntities(data.NetworkTechnologies, MapNetworkTechnologyDTOToEntity)

	// Convert NetworkElementTypes DTOs to entities
	networkElementTypes := MapToEntities(data.NetworkElementTypes, MapNetworkElementTypeDTOToEntity)

	// Convert ServiceTypes DTOs to entities
	serviceTypes := MapToEntities(data.ServiceTypes, MapServiceTypeDTOToEntity)

	// Return the lists of entities
	return networkTechnologies, networkElementTypes, serviceTypes, nil
}
