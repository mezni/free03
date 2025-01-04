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


