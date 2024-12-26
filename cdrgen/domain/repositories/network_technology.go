package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// NetworkTechnologyRepository defines the methods that any network technology repository should implement.
type NetworkTechnologyRepository interface {
    // Create inserts a single NetworkTechnology into the database.
    Create(tech entities.NetworkTechnology) entities.NetworkTechnology
    
    // CreateFromMapSlice takes a slice of maps and creates NetworkTechnology entities from it.
    CreateFromMapSlice(networkTechnologiesData []map[string]interface{}) ([]entities.NetworkTechnology, error)
    
    // FindByName retrieves a NetworkTechnology by its name.
    FindByName(name string) (entities.NetworkTechnology, bool)

    // FindAll retrieves all NetworkTechnologies from the database.
    FindAll() []entities.NetworkTechnology
    
    // GetMaxID retrieves the maximum ID currently assigned to NetworkTechnologies.
    GetMaxID() int
    
    // Close closes the database connection/resource.
    Close()
}