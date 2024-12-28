package main

import (
    "fmt"
    "log"

    "go.etcd.io/bbolt"
)

func main() {
    // Open the database
    db, err := bbolt.Open("network_data.db", 0600, nil)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Read data using a read-only transaction
    err = db.View(func(tx *bbolt.Tx) error {
        // Access the bucket
        bucket := tx.Bucket([]byte("NetworkTechnologies"))
        if bucket == nil {
            return fmt.Errorf("Bucket not found")
        }

        // Use a cursor to iterate through all key-value pairs
        cursor := bucket.Cursor()

        for k, v := cursor.First(); k != nil; k, v = cursor.Next() {
            // Print the key and value (assuming the value is a string)
            fmt.Printf("Key: %s, Value: %s\n", k, v)
        }

        return nil
    })

    if err != nil {
        log.Fatal(err)
    }
}