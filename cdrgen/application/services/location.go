package services

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/domain/repositories"
	"go.etcd.io/bbolt"
)

type LocationService struct {
	Repository   repositories.LocationRepository
	BoltDB       *bbolt.DB
	ConfigFile   map[string]interface{} 

// NewLocationService creates a new instance of LocationService.
func NewLocationService(repo repositories.LocationRepository, db *bbolt.DB, configFile map[string]interface{}) *LocationService {
	return &LocationService{
		Repository: repo,
		BoltDB:     db,
		ConfigFile: configFile,
	}
}

// ToDB loads configuration data from the ConfigFile and saves it to BoltDB.
func (s *LocationService) ToDB() error {
	if s.ConfigFile == nil {
		return fmt.Errorf("config file data is empty")
	}


}

// FromDB loads data from BoltDB to the in-memory repository
func (s *LocationService) FromDB() error {

}


