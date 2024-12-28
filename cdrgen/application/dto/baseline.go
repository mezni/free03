package dto

type ConfigData struct {
	NetworkTechnology []NetworkTechnologyDTO `json:"network_technology"`
	NetworkElementTypes   []NetworkElementTypeDTO    `json:"network_element_types"`
	ServiceTypes      []ServiceTypeDTO       `json:"service_types"`
}