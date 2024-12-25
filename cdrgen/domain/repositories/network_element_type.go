package repositories

// NetworkElementRepository defines the methods that any repository for NetworkElement should implement.
type NetworkElementRepository interface {
	// Create adds a new NetworkElement to the repository.
	Create(networkElement *NetworkElement) error
	
	// CreateMultiple adds multiple NetworkElements to the repository.
	CreateMultiple(networkElements []*NetworkElement) error
	
	// GetAll retrieves all NetworkElements in the repository.
	GetAll() ([]*NetworkElement, error)
	
	// GetRandomByNetworkType retrieves a random NetworkElement for a given NetworkType.
	GetRandomByNetworkType(networkType NetworkType) (*NetworkElement, error)
}
