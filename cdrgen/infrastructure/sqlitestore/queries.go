package sqlitestore

// Queries for creating tables.
const (
	CreateNetworkTechnologyTable = `
		CREATE TABLE IF NOT EXISTS network_technologies (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			Name TEXT NOT NULL,
			Description TEXT NOT NULL
		)`
	
	CreateNetworkElementTypeTable = `
		CREATE TABLE IF NOT EXISTS network_element_types (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			Name TEXT NOT NULL,
			Description TEXT NOT NULL,
			NetworkTechnology TEXT NOT NULL
		)`

	CreateServiceTypeTable = `
		CREATE TABLE IF NOT EXISTS service_types (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			Name TEXT NOT NULL,
			Description TEXT NOT NULL,
			NetworkTechnology TEXT NOT NULL
		)`
)

// Insert queries for each entity.
const (
	InsertNetworkTechnology = `
		INSERT INTO network_technologies (Name, Description) 
		VALUES (?, ?)`

	InsertNetworkElementType = `
		INSERT INTO network_element_types (Name, Description, NetworkTechnology) 
		VALUES (?, ?, ?)`

	InsertServiceType = `
		INSERT INTO service_types (Name, Description, NetworkTechnology) 
		VALUES (?, ?, ?)`
)

// Select queries for each entity.
const (
	SelectAllNetworkTechnologies = `
		SELECT id, Name, Description FROM network_technologies`
	
	SelectAllNetworkElementTypes = `
		SELECT id, Name, Description, NetworkTechnology FROM network_element_types`
	
	SelectAllServiceTypes = `
		SELECT id, Name, Description, NetworkTechnology FROM service_types`
)
