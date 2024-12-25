package bolt

import (
	"encoding/json"
	"errors"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/boltdb/bolt"
	"math/rand"
	"time"
)

var (
	ErrNetworkElementNotFound = errors.New("NetworkElement not found")
)

type BoltNetworkElementRepo struct {
	DB *bolt.DB
}

func NewBoltNetworkElementRepo(dbFilePath string) (*BoltNetworkElementRepo, error) {
	db, err := bolt.Open(dbFilePath, 0600, nil)
	if err != nil {
		return nil, err
	}

	repo := &BoltNetworkElementRepo{DB: db}
	err = repo.init()
	if err != nil {
		return nil, err
	}

	return repo, nil
}

// Initialize the bucket for storing NetworkElements
func (r *BoltNetworkElementRepo) init() error {
	return r.DB.Update(func(tx *bolt.Tx) error {
		_, err := tx.CreateBucketIfNotExists([]byte("NetworkElements"))
		return err
	})
}

// Create a new NetworkElement
func (r *BoltNetworkElementRepo) Create(ne *entities.NetworkElement) error {
	return r.DB.Update(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte("NetworkElements"))

		// Generate a unique ID for the NetworkElement
		networkElementID := rand.Int()

		ne.NetworkElementTypeID = networkElementID

		// Convert the NetworkElement to JSON and store it in the bucket
		data, err := json.Marshal(ne)
		if err != nil {
			return err
		}

		return b.Put([]byte(fmt.Sprintf("%d", networkElementID)), data)
	})
}

// CreateMultiple adds multiple NetworkElements to the repository
func (r *BoltNetworkElementRepo) CreateMultiple(neList []*entities.NetworkElement) error {
	return r.DB.Update(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte("NetworkElements"))

		for _, ne := range neList {
			networkElementID := rand.Int()
			ne.NetworkElementTypeID = networkElementID

			data, err := json.Marshal(ne)
			if err != nil {
				return err
			}

			err = b.Put([]byte(fmt.Sprintf("%d", networkElementID)), data)
			if err != nil {
				return err
			}
		}

		return nil
	})
}

// GetAll fetches all NetworkElements from the repository
func (r *BoltNetworkElementRepo) GetAll() ([]*entities.NetworkElement, error) {
	var networkElements []*entities.NetworkElement

	err := r.DB.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte("NetworkElements"))
		return b.ForEach(func(k, v []byte) error {
			var ne entities.NetworkElement
			err := json.Unmarshal(v, &ne)
			if err != nil {
				return err
			}
			networkElements = append(networkElements, &ne)
			return nil
		})
	})

	if err != nil {
		return nil, err
	}

	return networkElements, nil
}

// GetRandomByNetworkType fetches a random NetworkElement of a specified network type
func (r *BoltNetworkElementRepo) GetRandomByNetworkType(networkType entities.NetworkType) (*entities.NetworkElement, error) {
	var matchingElements []*entities.NetworkElement

	err := r.DB.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte("NetworkElements"))
		return b.ForEach(func(k, v []byte) error {
			var ne entities.NetworkElement
			err := json.Unmarshal(v, &ne)
			if err != nil {
				return err
			}
			if ne.NetworkType == networkType {
				matchingElements = append(matchingElements, &ne)
			}
			return nil
		})
	})

	if err != nil {
		return nil, err
	}

	if len(matchingElements) == 0 {
		return nil, ErrNetworkElementNotFound
	}

	// Return a random element from the matching ones
	rand.Seed(time.Now().UnixNano())
	randomIndex := rand.Intn(len(matchingElements))
	return matchingElements[randomIndex], nil
}
