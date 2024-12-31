
func main() {
	// Open or create the BoltDB database file
	
	db, err := bbolt.Open(dbFile, 0600, nil)
	if err != nil {
		log.Fatalf("Error opening BoltDB file: %v", err)
	}
	defer db.Close()

	// Example usage of the InitDBService with both configFile and the opened db connection
	service := NewInitDBService("config.json", db)

	// Initialize the database using the service
	if err := service.InitDB(); err != nil {
		log.Fatalf("Error initializing database: %v", err)
	}
}
