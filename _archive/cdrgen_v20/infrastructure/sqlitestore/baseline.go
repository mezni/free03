package sqlitestore

import (
	"database/sql"
	"log"

	_ "github.com/mattn/go-sqlite3" // SQLite driver
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// BaselineSQLiteRepository implements the repositories interfaces for SQLite.
type BaselineSQLiteRepository struct {
	db *sql.DB
}

// Open opens the database connection.
func (r *BaselineSQLiteRepository) Open(dbFile string) error {
	var err error
	r.db, err = sql.Open("sqlite3", dbFile)
	if err != nil {
		return err
	}

	// Verify that the connection is valid
	err = r.db.Ping()
	if err != nil {
		return err
	}
	log.Println("Database connection opened successfully")
	return nil
}

// Close closes the database connection.
func (r *BaselineSQLiteRepository) Close() error {
	if r.db != nil {
		err := r.db.Close()
		if err != nil {
			return err
		}
		log.Println("Database connection closed successfully")
	}
	return nil
}

// NewBaselineSQLiteRepository creates a new instance of BaselineSQLiteRepository.
func NewBaselineSQLiteRepository() *BaselineSQLiteRepository {
	return &BaselineSQLiteRepository{}
}

// CreateTables creates the necessary tables in the database if they don't exist.
func (r *BaselineSQLiteRepository) CreateTables() error {
	queries := []string{
		CreateNetworkTechnologyTable,
		CreateNetworkElementTypeTable,
		CreateServiceTypeTable,
	}

	for _, query := range queries {
		_, err := r.db.Exec(query)
		if err != nil {
			return err
		}
	}

	return nil
}

// Implementing NetworkTechnologyRepository interface.
func (r *BaselineSQLiteRepository) Insert(networkTechnology entities.NetworkTechnology) error {
	_, err := r.db.Exec(
		InsertNetworkTechnology,
		networkTechnology.Name, networkTechnology.Description,
	)
	return err
}

// Implementing GetAll method for NetworkTechnologyRepository.
func (r *BaselineSQLiteRepository) GetAll() ([]entities.NetworkTechnology, error) {
	rows, err := r.db.Query(SelectAllNetworkTechnologies)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var technologies []entities.NetworkTechnology
	for rows.Next() {
		var tech entities.NetworkTechnology
		if err := rows.Scan(&tech.ID, &tech.Name, &tech.Description); err != nil {
			return nil, err
		}
		technologies = append(technologies, tech)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return technologies, nil
}

// Implementing NetworkElementTypeRepository interface.
func (r *BaselineSQLiteRepository) Insert(networkElementType entities.NetworkElementType) error {
	_, err := r.db.Exec(
		InsertNetworkElementType,
		networkElementType.Name, networkElementType.Description, networkElementType.NetworkTechnology,
	)
	return err
}

// Implementing GetAll method for NetworkElementTypeRepository.
func (r *BaselineSQLiteRepository) GetAll() ([]entities.NetworkElementType, error) {
	rows, err := r.db.Query(SelectAllNetworkElementTypes)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var elements []entities.NetworkElementType
	for rows.Next() {
		var elem entities.NetworkElementType
		if err := rows.Scan(&elem.ID, &elem.Name, &elem.Description, &elem.NetworkTechnology); err != nil {
			return nil, err
		}
		elements = append(elements, elem)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return elements, nil
}

// Implementing ServiceTypeRepository interface.
func (r *BaselineSQLiteRepository) Insert(serviceType entities.ServiceType) error {
	_, err := r.db.Exec(
		InsertServiceType,
		serviceType.Name, serviceType.Description, serviceType.NetworkTechnology,
	)
	return err
}

// Implementing GetAll method for ServiceTypeRepository.
func (r *BaselineSQLiteRepository) GetAll() ([]entities.ServiceType, error) {
	rows, err := r.db.Query(SelectAllServiceTypes)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var services []entities.ServiceType
	for rows.Next() {
		var service entities.ServiceType
		if err := rows.Scan(&service.ID, &service.Name, &service.Description, &service.NetworkTechnology); err != nil {
			return nil, err
		}
		services = append(services, service)
	}
	if err := rows.Err(); err != nil {
		return nil, err
	}
	return services, nil
}
