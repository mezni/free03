package services

import (
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
)

// InitCacheService structure to hold service state
type InitCacheService struct {
	db *boltstore.BoltDBConfig
}

// NewInitCacheService constructor for InitCacheService
func NewInitCacheService() (*InitCacheService, error) {

	// Initialize BoltDBConfig and create the database file using the Create method
	boltDBConfig := boltstore.NewBoltDBConfig()
	if err := boltDBConfig.Open(dbPath); err != nil {
		return nil, err
	}

	return &InitCacheService{
		db: boltDBConfig,
	}, nil
}

func (service *InitCacheService) InitCache() error {
	return nil
}
