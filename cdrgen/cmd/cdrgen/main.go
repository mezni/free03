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
        // Iterate over all buckets
        return tx.ForEach(func(name []byte, b *bbolt.Bucket) error {
            fmt.Printf("Bucket: %s\n", name)

            // Use a cursor to iterate through all key-value pairs in the current bucket
            cursor := b.Cursor()
            for k, v := cursor.First(); k != nil; k, v = cursor.Next() {
                // Print the key and value for each entry
                fmt.Printf("  Key: %s, Value: %s\n", k, v)
            }

            return nil // continue to the next bucket
        })
    })

    if err != nil {
        log.Fatal(err)
    }
}