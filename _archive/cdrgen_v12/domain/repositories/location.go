package repositories



import 	"github.com/mezni/wovoka/cdrgen/domain/entities"


type LocationRepository interface {
    // Create adds a new Location to the repository.
    Create(location *entities.Location) error

    // Get retrieves a Location by its ID.
    Get(id int) (*entities.Location, error)
    
    // GetAll retrieves all Locations from the repository.
    GetAll() ([]*entities.Location, error)

    // GetRandomByNetworkTechnology retrieves a random Location by network technology.
    GetRandomByNetworkTechnology(networkTechnology string) (*entities.Location, error)
}