package boltstore

import (
    "log"

    "github.com/boltdb/bolt"
)

// BaseRepository provides common functionalities for BoltDB repositories
type BaseRepository struct {
    db         *bolt.DB
    bucketName string
}

// NewBaseRepository initializes a new BaseRepository with the given database path and bucket name.
func NewBaseRepository(dbPath string, bucketName string) (*BaseRepository, error) {
    db, err := bolt.Open(dbPath, 0600, nil)
    if err != nil {
        return nil, err
    }

    err = db.Update(func(tx *bolt.Tx) error {
        _, err := tx.CreateBucketIfNotExists([]byte(bucketName))
        return err
    })
    if err != nil {
        return nil, err
    }

    return &BaseRepository{db: db, bucketName: bucketName}, nil
}

// Close closes the database connection.
func (r *BaseRepository) Close() {
    r.db.Close()
}

// Serialize implements the serialization logic (to be defined).
func (r *BaseRepository) Serialize(data interface{}) ([]byte, error) {
    // Implement your serialization logic here (e.g., using JSON encoding)
    return nil, nil
}

// Deserialize implements the deserialization logic (to be defined).
func (r *BaseRepository) Deserialize(data []byte, result interface{}) error {
    // Implement your deserialization logic here (e.g., using JSON decoding)
    return nil
}

// Create inserts a new item into the bucket.
func (r *BaseRepository) Create(itemID int, item interface{}) (int, error) {
    err := r.db.Update(func(tx *bolt.Tx) error {
        b := tx.Bucket([]byte(r.bucketName))

        id, _ := b.NextSequence()
        itemID = int(id)
        data, err := r.Serialize(item)
        if err != nil {
            return err
        }

        return b.Put(itob(itemID), data)
    })

    if err != nil {
        log.Printf("Error creating item: %v", err)
        return 0, err
    }

    return itemID, nil
}

// CreateFromMapSlice creates multiple items from a slice of maps.
func (r *BaseRepository) CreateFromMapSlice(data []map[string]interface{}, createFunc func(item map[string]interface{}) (interface{}, error)) ([]interface{}, error) {
    var createdItems []interface{}

    for _, itemData := range data {
        createdItem, err := createFunc(itemData)
        if err == nil {
            createdItems = append(createdItems, createdItem)
        } else {
            log.Printf("Error creating item from map: %v", err)
        }
    }

    return createdItems, nil
}

// FindAll retrieves all items from the bucket.
func (r *BaseRepository) FindAll(result interface{}) error {
    err := r.db.View(func(tx *bolt.Tx) error {
        b := tx.Bucket([]byte(r.bucketName))

        return b.ForEach(func(k, v []byte) error {
            item := make(map[string]interface{})
            if err := r.Deserialize(v, &item); err == nil {
                // Append item to your result slice
            }
            return nil
        })
    })

    if err != nil {
        log.Printf("Error finding all items: %v", err)
        return err
    }

    return nil
}

// Utility functions to convert between int and byte slice
func itob(v int) []byte {
    return []byte{byte(v)} // Implement this for larger integers
}

func btoi(b []byte) int {
    return int(b[0]) // Implement this for larger integers
}