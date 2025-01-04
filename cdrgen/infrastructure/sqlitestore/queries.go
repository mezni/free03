package sqlitestore

const (
	CreateNetworkTechnologiesTable = `
		CREATE TABLE IF NOT EXISTS network_technologies (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL UNIQUE,
			description TEXT NOT NULL
		);`

	SelectNetworkTechnologiesByName = `
		SELECT id FROM network_technologies WHERE name = ?;`

	InsertNetworkTechnology = `
		INSERT INTO network_technologies (name, description)
		VALUES (?, ?);`

	SelectAllNetworkTechnologies = `
		SELECT id, name, description FROM network_technologies;`
)

const (
	CreateNetworkElementTypesTable = `
		CREATE TABLE IF NOT EXISTS network_element_types (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			description TEXT NOT NULL,
			network_technology INTEGER NOT NULL,
			FOREIGN KEY (network_technology) REFERENCES network_technologies(name) ON DELETE CASCADE
		);`

	SelectNetworkElementTypesByNameAndTech = `
		SELECT id FROM network_element_types WHERE name = ? AND network_technology = ?;`

	InsertNetworkElementType = `
		INSERT INTO network_element_types (name, description, network_technology)
		VALUES (?, ?, ?);`

	SelectAllNetworkElementTypes = `
		SELECT id, name, description, network_technology FROM network_element_types;`
)

const (
	CreateServiceTypesTable = `
		CREATE TABLE IF NOT EXISTS service_types (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			description TEXT NOT NULL,
			network_technology TEXT NOT NULL,
			bearer_type TEXT NOT NULL,
			jitter_min INTEGER NOT NULL,
			jitter_max INTEGER NOT NULL,
			latency_min INTEGER NOT NULL,
			latency_max INTEGER NOT NULL,
			throughput_min INTEGER NOT NULL,
			throughput_max INTEGER NOT NULL,
			packet_loss_min REAL NOT NULL,
			packet_loss_max REAL NOT NULL,
			call_setup_time_min INTEGER NOT NULL,
			call_setup_time_max INTEGER NOT NULL,
			mos_min REAL NOT NULL,
			mos_max REAL NOT NULL
		);`

	SelectServiceTypesByNameAndTech = `
		SELECT id FROM service_types WHERE name = ? AND network_technology = ?;`

	InsertServiceType = `
		INSERT INTO service_types (
			name, description, network_technology, bearer_type,
			jitter_min, jitter_max, latency_min, latency_max,
			throughput_min, throughput_max, packet_loss_min,
			packet_loss_max, call_setup_time_min, call_setup_time_max,
			mos_min, mos_max
		)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);`

	SelectAllServiceTypes = `
		SELECT id, name, description, network_technology, bearer_type,
			jitter_min, jitter_max, latency_min, latency_max,
			throughput_min, throughput_max, packet_loss_min,
			packet_loss_max, call_setup_time_min, call_setup_time_max,
			mos_min, mos_max
		FROM service_types;`
)

const (
	// SQL for creating the service_nodes table
	CreateServiceNodesTable = `
		CREATE TABLE IF NOT EXISTS service_nodes (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			service_name TEXT NOT NULL,
			network_technology TEXT NOT NULL
		);`

	// SQL for checking if a service node with the same name and network technology exists
	SelectServiceNodesByNameAndTechAndServ = `
		SELECT id FROM service_nodes WHERE name = ? AND network_technology = ? AND service_name = ?;`

	// SQL for inserting a new service node
	InsertServiceNode = `
		INSERT INTO service_nodes (name, service_name, network_technology)
		VALUES (?, ?, ?);`

	// SQL for selecting all service nodes
	SelectAllServiceNodes = `
		SELECT id, name, service_name, network_technology
		FROM service_nodes;`
)

const (
	CreateLocationsTable = `
		CREATE TABLE IF NOT EXISTS locations (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			latitude_min REAL NOT NULL,
			latitude_max REAL NOT NULL,
			longitude_min REAL NOT NULL,
			longitude_max REAL NOT NULL,
			area_code TEXT NOT NULL,
			network_technology TEXT NOT NULL
		);`

	SelectLocationsByNameAndTech = `
		SELECT id FROM locations WHERE name = ? AND network_technology = ?;`

	InsertLocation = `
		INSERT INTO locations (name, latitude_min, latitude_max, longitude_min, longitude_max, area_code, network_technology)
		VALUES (?, ?, ?, ?, ?, ?, ?);`

	SelectAllLocations = `
		SELECT id, name, latitude_min, latitude_max, longitude_min, longitude_max, area_code, network_technology FROM locations;`
)

const (
	// Create the table for network elements
	CreateNetworkElementsTable = `
	CREATE TABLE IF NOT EXISTS network_elements (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		name TEXT NOT NULL,
		description TEXT,
		network_technology TEXT NOT NULL,
		ip_address TEXT,
		status TEXT,
		tac TEXT,
		lac TEXT,
		cell_id TEXT
	);`

	// Insert a new network element
	InsertNetworkElement = `
	INSERT INTO network_elements 
	(name, description, network_technology, ip_address, status, tac, lac, cell_id)
	VALUES (?, ?, ?, ?, ?, ?, ?, ?);`

	// Select all network elements
	SelectAllNetworkElements = `
	SELECT id, name, description, network_technology, ip_address, status, tac, lac, cell_id
	FROM network_elements;`

	// Select network elements by name
	SelectNetworkElementByName = `
	SELECT id, name, description, network_technology, ip_address, status, tac, lac, cell_id
	FROM network_elements WHERE name = ?;`
)

const (
	// CreateTable for customers
	CreateCustomerTable = `
		CREATE TABLE IF NOT EXISTS customers (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			msisdn TEXT NOT NULL,
			imsi TEXT NOT NULL,
			imei TEXT NOT NULL,
			customer_type TEXT NOT NULL,
			account_type TEXT NOT NULL,
			status TEXT NOT NULL
		);`

	// Select by MSISDN to check if the customer exists
	SelectCustomerByMSISDN = `
		SELECT id FROM customers WHERE msisdn = ?;`

	// Insert a new customer
	InsertCustomer = `
		INSERT INTO customers (msisdn, imsi, imei, customer_type, account_type, status)
		VALUES (?, ?, ?, ?, ?, ?);`

	// Select all customers
	SelectAllCustomers = `
		SELECT id, msisdn, imsi, imei, customer_type, account_type, status FROM customers;`
)
