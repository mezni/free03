package dtos

// NetworkTechnology represents an entry in the network_technologies section.
type NetworkTechnologyDTO struct {
	Name        string `json:"Name"`
	Description string `json:"Description"`
}

// NetworkElementType represents an entry in the network_element_types section.
type NetworkElementTypeDTO struct {
	Name           string `json:"Name"`
	Description    string `json:"Description"`
	NetworkTechnology string `json:"NetworkTechnology"`
}

// ServiceType represents an entry in the service_types section.
type ServiceTypeDTO struct {
	Name            string `json:"Name"`
	Description     string `json:"Description"`
	NetworkTechnology string `json:"NetworkTechnology"`
}

// Data represents the overall structure of the JSON file.
type BaselineData struct {
	NetworkTechnologies []NetworkTechnologyDTO   `json:"network_technologies"`
	NetworkElementTypes []NetworkElementTypeDTO  `json:"network_element_types"`
	ServiceTypes        []ServiceTypeDTO         `json:"service_types"`
}