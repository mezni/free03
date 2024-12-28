package repositories

import (
	"encoding/json"
	"fmt"
	"go.etcd.io/bbolt"
)

// BoltDBLocationRepository is a BoltDB implementation of the LocationRepository interface.
type BoltDBLocationRepository struct {
	DB *bbolt.DB
}

// NewBoltDBLocationRepository creates a new instance of BoltDBLocationRepository.
func NewBoltDBLocationRepository(db *bbolt.DB) *BoltDBLocationRepository {
	return &BoltDBLocationRepository{
		DB: db,
	}

