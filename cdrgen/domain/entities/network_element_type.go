package entities

// NetworkElement represents a network element with type, name, and description.
type NetworkElement struct {
	NetworkElementTypeID int
	NetworkType          NetworkType
	NetworkElementName   string
	NetworkElementDesc   *string
}

// NewNetworkElement is a factory function to create a new NetworkElement instance.
func NewNetworkElement(
	networkElementTypeID int,
	networkType NetworkType,
	networkElementName string,
	networkElementDesc *string,
) (*NetworkElement, error) {
	// Validate network type
	if !IsValidNetworkType(networkType) {
		return nil, ErrInvalidNetworkType
	}

	// Validate that NetworkElementName is not empty
	if networkElementName == "" {
		return nil, ErrEmptyNetworkElementName
	}

	// Return the new NetworkElement instance
	return &NetworkElement{
		NetworkElementTypeID: networkElementTypeID,
		NetworkType:          networkType,
		NetworkElementName:   networkElementName,
		NetworkElementDesc:   networkElementDesc,
	}, nil
}
