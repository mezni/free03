package services

import (
	"database/sql"
	"fmt"
	"gopkg.in/yaml.v3"
	"io/ioutil"
	"log"

	"github.com/mezni/wovoka/cdrgen/application/interfaces"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/domain/factories"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
)

type LoaderService struct {
	DB                     *sql.DB
	NetworkTechRepo        *sqlitestore.NetworkTechnologyRepository
	NetworkElementTypeRepo *sqlitestore.NetworkElementTypeRepository
	ServiceTypeRepo        *sqlitestore.ServiceTypeRepository
	ServiceNodeRepo        *sqlitestore.ServiceNodeRepository
	LocationRepo           *sqlitestore.LocationRepository
	NetworkElementRepo     *sqlitestore.NetworkElementRepository
	CustomerRepo     *sqlitestore.CustomerRepository
}

// NewLoaderService initializes the LoaderService with all repositories.
func NewLoaderService(dbFile string) (*LoaderService, error) {
	db, err := sql.Open("sqlite3", dbFile)
	if err != nil {
		return nil, fmt.Errorf("could not open database: %v", err)
	}

	if err := db.Ping(); err != nil {
		db.Close()
		return nil, fmt.Errorf("could not connect to database: %v", err)
	}

	return &LoaderService{
		DB:                     db,
		NetworkTechRepo:        sqlitestore.NewNetworkTechnologyRepository(db),
		NetworkElementTypeRepo: sqlitestore.NewNetworkElementTypeRepository(db),
		ServiceTypeRepo:        sqlitestore.NewServiceTypeRepository(db),
		ServiceNodeRepo:        sqlitestore.NewServiceNodeRepository(db),
		LocationRepo:           sqlitestore.NewLocationRepository(db),
		NetworkElementRepo:     sqlitestore.NewNetworkElementRepository(db),
		CustomerRepo:     sqlitestore.NewCustomerRepository(db),
	}, nil
}

// SetupDatabase creates all necessary tables.
func (l *LoaderService) SetupDatabase() error {
	if err := l.NetworkTechRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create network technology table: %v", err)
	}
	if err := l.NetworkElementTypeRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create network element type table: %v", err)
	}
	if err := l.ServiceTypeRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create service type table: %v", err)
	}
	if err := l.ServiceNodeRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create service node table: %v", err)
	}
	if err := l.LocationRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create locations table: %v", err)
	}
	if err := l.NetworkElementRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create network elements table: %v", err)
	}
	if err := l.CustomerRepo.CreateTable(); err != nil {
		return fmt.Errorf("failed to create customers table: %v", err)
	}
	log.Println("All tables created successfully.")
	return nil
}

// LoadNetworkTechnologies processes and inserts NetworkTechnologies into the database.
func (l *LoaderService) LoadNetworkTechnologies(networkTechnologies []interfaces.NetworkTechnology) error {
	tx, err := l.DB.Begin()
	if err != nil {
		return fmt.Errorf("could not begin transaction: %v", err)
	}

	for _, nt := range networkTechnologies {
		entity := entities.NetworkTechnology{
			Name:        nt.Name,
			Description: nt.Description,
		}
		if err := l.NetworkTechRepo.Insert(entity); err != nil {
			tx.Rollback()
			return fmt.Errorf("error saving network technology %s: %v", entity.Name, err)
		}
		log.Printf("Successfully inserted network technology: %s", entity.Name)
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("could not commit transaction: %v", err)
	}

	log.Printf("Successfully inserted %d network technologies", len(networkTechnologies))
	return nil
}

// LoadNetworkElementTypes processes and inserts NetworkElementTypes into the database.
func (l *LoaderService) LoadNetworkElementTypes(networkElementTypes []interfaces.NetworkElementType) error {
	tx, err := l.DB.Begin()
	if err != nil {
		return fmt.Errorf("could not begin transaction: %v", err)
	}

	for _, ne := range networkElementTypes {
		entity := entities.NetworkElementType{
			Name:              ne.Name,
			Description:       ne.Description,
			NetworkTechnology: ne.NetworkTechnology,
		}
		if err := l.NetworkElementTypeRepo.Insert(entity); err != nil {
			tx.Rollback()
			return fmt.Errorf("error saving network element type %s: %v", entity.Name, err)
		}
		log.Printf("Successfully inserted network element type: %s", entity.Name)
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("could not commit transaction: %v", err)
	}

	log.Printf("Successfully inserted %d network element types", len(networkElementTypes))
	return nil
}

// LoadServiceTypes processes and inserts ServiceTypes into the database.
func (l *LoaderService) LoadServiceTypes(serviceTypes []interfaces.ServiceType) error {
	tx, err := l.DB.Begin()
	if err != nil {
		return fmt.Errorf("could not begin transaction: %v", err)
	}

	for _, st := range serviceTypes {
		entity := entities.ServiceType{
			Name:              st.Name,
			Description:       st.Description,
			NetworkTechnology: st.NetworkTechnology,
			BearerType:        st.BearerType,
			JitterMin:         st.JitterMin,
			JitterMax:         st.JitterMax,
			LatencyMin:        st.LatencyMin,
			LatencyMax:        st.LatencyMax,
			ThroughputMin:     st.ThroughputMin,
			ThroughputMax:     st.ThroughputMax,
			PacketLossMin:     st.PacketLossMin,
			PacketLossMax:     st.PacketLossMax,
			CallSetupTimeMin:  st.CallSetupTimeMin,
			CallSetupTimeMax:  st.CallSetupTimeMax,
			MosMin:            st.MosMin,
			MosMax:            st.MosMax,
		}
		if err := l.ServiceTypeRepo.Insert(entity); err != nil {
			tx.Rollback()
			return fmt.Errorf("error saving service type %s: %v", entity.Name, err)
		}
		log.Printf("Successfully inserted service type: %s", entity.Name)
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("could not commit transaction: %v", err)
	}

	log.Printf("Successfully inserted %d service types", len(serviceTypes))
	return nil
}

// LoadServiceNodes processes and inserts ServiceNodes into the database.
func (l *LoaderService) LoadServiceNodes(serviceNodes []interfaces.ServiceNode) error {
	tx, err := l.DB.Begin()
	if err != nil {
		return fmt.Errorf("could not begin transaction: %v", err)
	}

	for _, sn := range serviceNodes {
		entity := entities.ServiceNode{
			Name:              sn.Name,
			ServiceName:       sn.ServiceName,
			NetworkTechnology: sn.NetworkTechnology,
		}
		if err := l.ServiceNodeRepo.Insert(entity); err != nil {
			tx.Rollback()
			return fmt.Errorf("error saving service node %s: %v", entity.Name, err)
		}
		log.Printf("Successfully inserted service node: %s", entity.Name)
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("could not commit transaction: %v", err)
	}

	log.Printf("Successfully inserted %d service nodes", len(serviceNodes))
	return nil
}

// LoadLocations processes and inserts Locations into the database.
func (l *LoaderService) LoadLocations(locations []entities.Location) error {
	tx, err := l.DB.Begin()
	if err != nil {
		return fmt.Errorf("could not begin transaction: %v", err)
	}

	for _, loc := range locations {
		if err := l.LocationRepo.Insert(loc); err != nil {
			tx.Rollback()
			return fmt.Errorf("error saving location %s: %v", loc.Name, err)
		}
		log.Printf("Successfully inserted location: %s", loc.Name)
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("could not commit transaction: %v", err)
	}

	log.Printf("Successfully inserted %d locations", len(locations))
	return nil
}

// LoadNetworkElements processes and inserts NetworkElements into the database.
func (l *LoaderService) LoadNetworkElements(networkElements []entities.NetworkElement) error {
	tx, err := l.DB.Begin()
	if err != nil {
		return fmt.Errorf("could not begin transaction: %v", err)
	}

	for _, ne := range networkElements {
		if err := l.NetworkElementRepo.Insert(ne); err != nil {
			tx.Rollback()
			return fmt.Errorf("error saving network element %s: %v", ne.Name, err)
		}
		log.Printf("Successfully inserted network element: %s", ne.Name)
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("could not commit transaction: %v", err)
	}

	log.Printf("Successfully inserted %d network elements", len(networkElements))
	return nil
}

func (l *LoaderService) LoadCustomers(customers []entities.Customer) error {
	tx, err := l.DB.Begin()
	if err != nil {
		return fmt.Errorf("could not begin transaction: %v", err)
	}

	for _, cus := range customers {
		if err := l.CustomerRepo.Insert(cus); err != nil {
			tx.Rollback()
			return fmt.Errorf("error saving customer %s: %v", cus.MSISDN, err)
		}
		log.Printf("Successfully inserted customer: %s", cus.MSISDN)
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("could not commit transaction: %v", err)
	}

	log.Printf("Successfully inserted %d customers", len(customers))
	return nil
}

func (l *LoaderService) Load(yamlFilename string) error {
	data, err := ioutil.ReadFile(yamlFilename)
	if err != nil {
		return fmt.Errorf("could not read YAML file: %v", err)
	}

	var businessConfig mappers.BusinessConfig
	if err := yaml.Unmarshal(data, &businessConfig); err != nil {
		return fmt.Errorf("could not unmarshal YAML: %v", err)
	}

	// Setup the database
	if err := l.SetupDatabase(); err != nil {
		return fmt.Errorf("failed to set up database tables: %v", err)
	}

	// Load JSON data
	jsonData, err := interfaces.ReadConfig()
	if err != nil {
		return fmt.Errorf("could not read JSON file: %v", err)
	}

	// Load various entities
	if err := l.LoadNetworkTechnologies(jsonData.NetworkTechnologies); err != nil {
		return fmt.Errorf("failed to load network technologies: %v", err)
	}
	if err := l.LoadNetworkElementTypes(jsonData.NetworkElementTypes); err != nil {
		return fmt.Errorf("failed to load network element types: %v", err)
	}
	if err := l.LoadServiceTypes(jsonData.ServiceTypes); err != nil {
		return fmt.Errorf("failed to load service types: %v", err)
	}
	if err := l.LoadServiceNodes(jsonData.ServiceNodes); err != nil {
		return fmt.Errorf("failed to load service nodes: %v", err)
	}

	locations, err := factories.GenerateLocations(&businessConfig)
	if err != nil {
		return fmt.Errorf("error generating locations: %v", err)
	}

	// Convert []*entities.Location to []entities.Location
	convertedLocations := make([]entities.Location, len(locations))
	for i, loc := range locations {
		if loc != nil {
			convertedLocations[i] = *loc // Dereference the pointer
		}
	}

	// Load locations
	if err := l.LoadLocations(convertedLocations); err != nil {
		return fmt.Errorf("failed to load locations: %v", err)
	}

	networkElementTypesList, err := l.NetworkElementTypeRepo.GetAll()
	if err != nil {
		return fmt.Errorf("failed to get network element types: %v", err)
	}

	locationsList, err := l.LocationRepo.GetAll()
	if err != nil {
		return fmt.Errorf("failed to get locations: %v", err)
	}

	// Convert []entities.NetworkElementType to []*entities.NetworkElementType
	networkElementTypesListPointers := make([]*entities.NetworkElementType, len(networkElementTypesList))
	for i, netElemType := range networkElementTypesList {
		networkElementTypesListPointers[i] = &netElemType
	}

	// Convert []entities.Location to []*entities.Location
	locationsListPointers := make([]*entities.Location, len(locationsList))
	for i, loc := range locationsList {
		locationsListPointers[i] = &loc
	}

	// Now pass the converted slices to GenerateNetworkElements
	networkElements, err := factories.GenerateNetworkElements(networkElementTypesListPointers, locationsListPointers)
	if err != nil {
		return fmt.Errorf("error generating network elements: %v", err)
	}

	// Convert []*entities.NetworkElement to []entities.NetworkElement
	convertedNetworkElements := make([]entities.NetworkElement, len(networkElements))
	for i, ne := range networkElements {
		if ne != nil {
			convertedNetworkElements[i] = *ne // Dereference the pointer
		}
	}

	// Load network elements
	if err := l.LoadNetworkElements(convertedNetworkElements); err != nil {
		return fmt.Errorf("failed to load network elements: %v", err)
	}

	customers, err := factories.GenerateCustomers(&businessConfig)
	if err != nil {
		return fmt.Errorf("error generating customers: %v", err)
	}

	convertedCustomers := make([]entities.Customer, len(customers))
	for i, cus := range customers {
		if cus != nil {
			convertedCustomers[i] = *cus 
		}
	}

	if err := l.LoadCustomers(convertedCustomers); err != nil {
		return fmt.Errorf("failed to load customers: %v", err)
	}

	return nil
}

// Close closes the database connection.
func (l *LoaderService) Close() error {
	if l.DB != nil {
		err := l.DB.Close()
		if err != nil {
			log.Printf("Error closing database connection: %v", err)
			return err
		}
		log.Println("Database connection closed successfully.")
	}
	return nil
}
