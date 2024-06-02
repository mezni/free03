package sqlite

var TablesCreateStmt = []string{
	`CREATE TABLE IF NOT EXISTS services (
            service_id TEXT PRIMARY KEY,
            service_name TEXT NOT NULL
        );`,
	`CREATE TABLE IF NOT EXISTS expenses (
            expense_id TEXT PRIMARY KEY,
            service_id TEXT NOT NULL,
            amount TEXT NOT NULL           
        );`}
