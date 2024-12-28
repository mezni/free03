package dto

type ConfigData struct {
	NetworkTechnologies   []NetworkTechnologyDTO  `json:"network_technologies"`
	NetworkElementTypes []NetworkElementTypeDTO `json:"network_element_types"`
	ServiceTypes        []ServiceTypeDTO        `json:"service_types"`
}
