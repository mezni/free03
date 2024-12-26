package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// NetworkElementTypeRepository defines the methods that any network element type repository should implement.
type NetworkElementTypeRepository interface {
    // Create inserts a single NetworkElementType into the database and returns the created entity.
    // Returns an error if something goes wrong.
    Create(element entities.NetworkElementType) (entities.NetworkElementType, error)

    // CreateMany takes a slice of NetworkElementType entities and inserts them into the database.
    // Returns a slice of created entities and an error if something goes wrong.
    CreateMany(networkElementTypes []entities.NetworkElementType) ([]entities.NetworkElementType, error)

    // FindByName retrieves a NetworkElementType by its name.
    // Returns the entity and a boolean indicating whether it was found.
    FindByName(name string) (entities.NetworkElementType, bool, error)

    // FindAll retrieves all NetworkElementTypes from the database.
    // Returns a slice of entities and an error if something goes wrong.
    FindAll() ([]entities.NetworkElementType, error)

    // GetMaxID retrieves the maximum ID currently assigned to NetworkElementTypes.
    // Returns the maximum ID and an error if something goes wrong.
    GetMaxID() (int, error)
}
