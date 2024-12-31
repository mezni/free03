package dtos

type NetworkTechnologyDTO struct {
	Name        string `json:"Name"`
	Description string `json:"Description"`
}

type NetworkElementTypeDTO struct {
	Name              string `json:"Name"`
	Description       string `json:"Description"`
	NetworkTechnology string `json:"NetworkTechnology"`
}

type ServiceTypeDTO struct {
	Name              string `json:"Name"`
	Description       string `json:"Description"`
	NetworkTechnology string `json:"NetworkTechnology"`
}

type BaselineConfig struct {
	NetworkTechnologies []NetworkTechnologyDTO  `json:"network_technologies"`
	NetworkElementTypes []NetworkElementTypeDTO `json:"network_element_types"`
	ServiceTypes        []ServiceTypeDTO        `json:"service_types"`
}