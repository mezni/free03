package sqlitestore

import (
	"encoding/json"
	"database/sql"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
//	"log"
)

// ServiceTypeRepository handles database operations for service types.
type ServiceTypeRepository struct {
	db *sql.DB
}

// NewServiceTypeRepository creates a new instance of ServiceTypeRepository.
func NewServiceTypeRepository(db *sql.DB) *ServiceTypeRepository {
	return &ServiceTypeRepository{db: db}
}

// CreateTable creates the service_types table with lowercase column names.
func (r *ServiceTypeRepository) CreateTable() error {
	query := `
		CREATE TABLE IF NOT EXISTS service_types (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			description TEXT NOT NULL,
			network_technology TEXT NOT NULL,
			nodes TEXT NOT NULL, -- JSON string
			bearer_type TEXT NOT NULL,
			jitter_min INTEGER NOT NULL,
			jitter_max INTEGER NOT NULL,
			latency_min INTEGER NOT NULL,
			latency_max INTEGER NOT NULL,
			throughput_min INTEGER NOT NULL,
			throughput_max INTEGER NOT NULL,
			packet_loss_min INTEGER NOT NULL,
			packet_loss_max INTEGER NOT NULL,
			call_setup_time_min INTEGER NOT NULL,
			call_setup_time_max INTEGER NOT NULL,
			mos_range_min REAL NOT NULL,
			mos_range_max REAL NOT NULL
		)`
	_, err := r.db.Exec(query)
	return err
}



// Insert inserts a new service type into the database, but does not insert if a duplicate exists.
func (r *ServiceTypeRepository) Insert(serviceType entities.ServiceType) error {
	nodesJSON, err := json.Marshal(serviceType.Nodes)
	if err != nil {
		return err
	}

	query := `
		INSERT INTO service_types (
			name, description, network_technology, nodes, bearer_type, 
			jitter_min, jitter_max, latency_min, latency_max, 
			throughput_min, throughput_max, packet_loss_min, packet_loss_max, 
			call_setup_time_min, call_setup_time_max, mos_range_min, mos_range_max
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`
	_, err = r.db.Exec(query,
		serviceType.Name,
		serviceType.Description,
		serviceType.NetworkTechnology,
		nodesJSON,
		serviceType.BearerType,
		serviceType.JitterMin,
		serviceType.JitterMax,
		serviceType.LatencyMin,
		serviceType.LatencyMax,
		serviceType.ThroughputMin,
		serviceType.ThroughputMax,
		serviceType.PacketLossMin,
		serviceType.PacketLossMax,
		serviceType.CallSetupTimeMin,
		serviceType.CallSetupTimeMax,
		serviceType.MosRangeMin,
		serviceType.MosRangeMax,
	)
	return err
}


// GetAll retrieves all service types from the database.
func (r *ServiceTypeRepository) GetAll() ([]entities.ServiceType, error) {
	rows, err := r.db.Query(`
		SELECT id, name, description, network_technology, nodes, bearer_type,
		jitter_min, jitter_max, latency_min, latency_max, 
		throughput_min, throughput_max, packet_loss_min, packet_loss_max, 
		call_setup_time_min, call_setup_time_max, mos_range_min, mos_range_max 
		FROM service_types`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var services []entities.ServiceType
	for rows.Next() {
		var service entities.ServiceType
		var nodesJSON string

		err := rows.Scan(
			&service.ID, &service.Name, &service.Description, &service.NetworkTechnology,
			&nodesJSON, &service.BearerType,
			&service.JitterMin, &service.JitterMax,
			&service.LatencyMin, &service.LatencyMax,
			&service.ThroughputMin, &service.ThroughputMax,
			&service.PacketLossMin, &service.PacketLossMax,
			&service.CallSetupTimeMin, &service.CallSetupTimeMax,
			&service.MosRangeMin, &service.MosRangeMax,
		)
		if err != nil {
			return nil, err
		}

		err = json.Unmarshal([]byte(nodesJSON), &service.Nodes)
		if err != nil {
			return nil, err
		}

		services = append(services, service)
	}
	return services, nil
}
