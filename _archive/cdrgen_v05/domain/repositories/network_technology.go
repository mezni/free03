package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// NetworkTechnologyRepository defines the methods that any network technology repository should implement.
type NetworkTechnologyRepository interface {
    // Create inserts a single NetworkTechnology into the database and returns the created entity.
    // Returns an error if something goes wrong.
    Create(tech entities.NetworkTechnology) (entities.NetworkTechnology, error)
    
    // CreateFromMapSlice takes a slice of maps and creates NetworkTechnology entities from it.
    // Returns a slice of created entities and an error in case of failure.
    CreateFromMapSlice(networkTechnologiesData []map[string]interface{}) ([]entities.NetworkTechnology, error)
    
    // FindByName retrieves a NetworkTechnology by its name.
    // Returns the entity and a boolean indicating whether it was found.
    FindByName(name string) (entities.NetworkTechnology, bool, error)

    // FindAll retrieves all NetworkTechnologies from the database.
    // Returns a slice of entities and an error if something goes wrong.
    FindAll() ([]entities.NetworkTechnology, error)
    
    // GetMaxID retrieves the maximum ID currently assigned to NetworkTechnologies.
    // Returns the maximum ID and an error if something goes wrong.
    GetMaxID() (int, error)
}
