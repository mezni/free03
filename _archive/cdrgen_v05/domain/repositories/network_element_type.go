package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// NetworkElementTypeRepository defines the methods that any network element type repository should implement.
type NetworkElementTypeRepository interface {
    // Create inserts a single NetworkElementType into the database.
    Create(element entities.NetworkElementType) entities.NetworkElementType
    
    // CreateFromMapSlice takes a slice of maps and creates NetworkElementType entities from it.
    CreateFromMapSlice(elementData []map[string]interface{}) ([]entities.NetworkElementType, error)
    
    // FindByName retrieves a NetworkElementType by its name.
    FindByName(name string) (entities.NetworkElementType, bool)

    // FindAll retrieves all NetworkElementTypes from the database.
    FindAll() []entities.NetworkElementType
    
    // GetMaxID retrieves the maximum ID currently assigned to NetworkElementTypes.
    GetMaxID() int
    
    // Close closes the database connection/resource.
    Close()
}