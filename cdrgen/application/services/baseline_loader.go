package services

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"os"

	"github.com/boltdb/bolt"
	"github.com/mezni/wovoka/cdrgen/application/dto"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// BaselineLoaderService defines the service for loading baseline data
type BaselineLoaderService struct {
	DB *bolt.DB // BoltDB instance to persist data (you can swap with another DB)
}

// LoadData loads baseline data from a JSON file and processes it
func (b *BaselineLoaderService) LoadData(filename string) error {
	// Open the JSON file
	file, err := os.Open(filename)
	if err != nil {
		return fmt.Errorf("error opening file: %v", err)
	}
	defer file.Close()

	// Read the file into a byte slice
	byteValue, err := ioutil.ReadAll(file)
	if err != nil {
		return fmt.Errorf("error reading file: %v", err)
	}

	// Declare a variable to hold the unmarshaled JSON
	var data dto.ConfigData

	// Unmarshal the JSON data into the struct
	err = json.Unmarshal(byteValue, &data)
	if err != nil {
		return fmt.Errorf("error unmarshaling data: %v", err)
	}

	// Process each entity
	if err := b.processNetworkTechnologies(data.NetworkTechnology); err != nil {
		return fmt.Errorf("error processing network technologies: %v", err)
	}

	if err := b.processNetworkElementTypes(data.NetworkElementTypes); err != nil {
		return fmt.Errorf("error processing network elements: %v", err)
	}

	if err := b.processServiceTypes(data.ServiceTypes); err != nil {
		return fmt.Errorf("error processing service types: %v", err)
	}

	return nil
}

// Process Network Technologies
func (b *BaselineLoaderService) processNetworkTechnologies(networkTechnologies []dto.NetworkTechnologyDTO) error {
	idseq := 1
	for _, nt := range networkTechnologies {
		// Create domain model
		ntInstance := entities.NetworkTechnology{
			ID:          idseq,
			Name:        nt.Name,
			Description: nt.Description,
		}

		// Save to DB
		if err := b.saveToDB("NetworkTechnologies", ntInstance.ID, ntInstance); err != nil {
			return fmt.Errorf("error saving network technology: %v", err)
		}
		idseq++
	}
	return nil
}

// Process Network Elements
func (b *BaselineLoaderService) processNetworkElementTypes(NetworkElementTypes []dto.NetworkElementTypeDTO) error {
	idseq := 1
	for _, ne := range NetworkElementTypes {
		// Create domain model
		neInstance := entities.NetworkElementType{
			ID:                idseq,
			Name:              ne.Name,
			Description:       ne.Description,
			NetworkTechnology: ne.NetworkTechnology,
		}

		// Save to DB
		if err := b.saveToDB("NetworkElementTypes", neInstance.ID, neInstance); err != nil {
			return fmt.Errorf("error saving network element: %v", err)
		}
		idseq++
	}
	return nil
}

// Process Service Types
func (b *BaselineLoaderService) processServiceTypes(serviceTypes []dto.ServiceTypeDTO) error {
	idseq := 1
	for _, st := range serviceTypes {
		// Create domain model
		stInstance := entities.ServiceType{
			ID:                idseq,
			Name:              st.Name,
			Description:       st.Description,
			NetworkTechnology: st.NetworkTechnology,
		}

		// Save to DB
		if err := b.saveToDB("ServiceTypes", stInstance.ID, stInstance); err != nil {
			return fmt.Errorf("error saving service type: %v", err)
		}
		idseq++
	}
	return nil
}

// Save the entity data to the DB (using BoltDB as an example)
func (b *BaselineLoaderService) saveToDB(bucketName string, key int, data interface{}) error {
	err := b.DB.Update(func(tx *bolt.Tx) error {
		// Create or get the bucket
		bucket, err := tx.CreateBucketIfNotExists([]byte(bucketName))
		if err != nil {
			return err
		}

		// Marshal the struct into JSON
		jsonData, err := json.Marshal(data)
		if err != nil {
			return err
		}

		// Save the data in the bucket
		err = bucket.Put([]byte(fmt.Sprintf("%d", key)), jsonData)
		return err
	})
	return err
}
