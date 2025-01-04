package services

import (
	"database/sql"
	"fmt"
	"log"

	"github.com/mezni/wovoka/cdrgen/application/interfaces"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
)

type LoaderService struct {
	DB                     *sql.DB
	NetworkTechRepo        *sqlitestore.NetworkTechnologyRepository
	NetworkElementTypeRepo *sqlitestore.NetworkElementTypeRepository
	ServiceTypeRepo        *sqlitestore.ServiceTypeRepository
	ServiceNodeRepo        *sqlitestore.ServiceNodeRepository
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

// Load reads JSON data and loads them into the database.
func (l *LoaderService) Load() error {
	// Step 1: Setup the database (create necessary tables)
	if err := l.SetupDatabase(); err != nil {
		return fmt.Errorf("failed to set up database tables: %v", err)
	}

	// Step 2: Read JSON data from the file
	jsonData, err := interfaces.ReadConfig()
	if err != nil {
		return fmt.Errorf("could not read JSON file: %v", err)
	}

	// Step 3: Load Network Technologies
	log.Printf("Started loading %d network technologies", len(jsonData.NetworkTechnologies))
	if err := l.LoadNetworkTechnologies(jsonData.NetworkTechnologies); err != nil {
		return fmt.Errorf("failed to load network technologies: %v", err)
	}

	// Step 4: Load Network Element Types
	log.Printf("Started loading %d network element types", len(jsonData.NetworkElementTypes))
	if err := l.LoadNetworkElementTypes(jsonData.NetworkElementTypes); err != nil {
		return fmt.Errorf("failed to load network element types: %v", err)
	}

	// Step 5: Load Service Types
	log.Printf("Started loading %d service types", len(jsonData.ServiceTypes))
	if err := l.LoadServiceTypes(jsonData.ServiceTypes); err != nil {
		return fmt.Errorf("failed to load service types: %v", err)
	}

	// Step 6: Load Service Nodes
	log.Printf("Started loading %d service nodes", len(jsonData.ServiceNodes))
	if err := l.LoadServiceNodes(jsonData.ServiceNodes); err != nil {
		return fmt.Errorf("failed to load service nodes: %v", err)
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
