package sqlitestore

// SQL Queries for Network Technologies
const (
	CreateNetworkTechnologiesTable = `
		CREATE TABLE IF NOT EXISTS network_technologies (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
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
