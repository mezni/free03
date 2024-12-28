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

// LoadData loads baseline data from a JSON file, processes it, and saves it to the database
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

	// Process and save Network Technologies
	networkTechnologyList, err := b.processNetworkTechnologies(data.NetworkTechnologies)
	if err != nil {
		return fmt.Errorf("error processing network technologies: %v", err)
	}
	if err := b.saveListToDB("NetworkTechnologies", networkTechnologyList); err != nil {
		return fmt.Errorf("error saving network technology list: %v", err)
	}

	// Process and save Network Element Types
	networkElementTypeList, err := b.processNetworkElementTypes(data.NetworkElementTypes)
	if err != nil {
		return fmt.Errorf("error processing network element types: %v", err)
	}
	if err := b.saveListToDB("NetworkElementTypes", networkElementTypeList); err != nil {
		return fmt.Errorf("error saving network element type list: %v", err)
	}

	// Process and save Service Types
	serviceTypeList, err := b.processServiceTypes(data.ServiceTypes)
	if err != nil {
		return fmt.Errorf("error processing service types: %v", err)
	}
	if err := b.saveListToDB("ServiceTypes", serviceTypeList); err != nil {
		return fmt.Errorf("error saving service type list: %v", err)
	}

	return nil
}

// Process Network Technologies and return the list
func (b *BaselineLoaderService) processNetworkTechnologies(networkTechnologies []dto.NetworkTechnologyDTO) ([]entities.NetworkTechnology, error) {
	var networkTechnologyList []entities.NetworkTechnology
	idseq := 1

	// Loop through and create domain models
	for _, nt := range networkTechnologies {
		ntInstance := entities.NetworkTechnology{
			ID:          idseq,
			Name:        nt.Name,
			Description: nt.Description,
		}
		networkTechnologyList = append(networkTechnologyList, ntInstance)
		idseq++
	}

	return networkTechnologyList, nil
}

// Process Network Element Types and return the list
func (b *BaselineLoaderService) processNetworkElementTypes(networkElementTypes []dto.NetworkElementTypeDTO) ([]entities.NetworkElementType, error) {
	var networkElementTypeList []entities.NetworkElementType
	idseq := 1

	// Loop through and create domain models
	for _, ne := range networkElementTypes {
		neInstance := entities.NetworkElementType{
			ID:                idseq,
			Name:              ne.Name,
			Description:       ne.Description,
			NetworkTechnology: ne.NetworkTechnology,
		}
		networkElementTypeList = append(networkElementTypeList, neInstance)
		idseq++
	}

	return networkElementTypeList, nil
}

// Process Service Types and return the list
func (b *BaselineLoaderService) processServiceTypes(serviceTypes []dto.ServiceTypeDTO) ([]entities.ServiceType, error) {
	var serviceTypeList []entities.ServiceType
	idseq := 1

	// Loop through and create domain models
	for _, st := range serviceTypes {
		stInstance := entities.ServiceType{
			ID:                idseq,
			Name:              st.Name,
			Description:       st.Description,
			NetworkTechnology: st.NetworkTechnology,
		}
		serviceTypeList = append(serviceTypeList, stInstance)
		idseq++
	}

	return serviceTypeList, nil
}

// Save a list of entities to the DB (using BoltDB as an example)
func (b *BaselineLoaderService) saveListToDB(bucketName string, dataList interface{}) error {
	err := b.DB.Update(func(tx *bolt.Tx) error {
		// Create or get the bucket
		bucket, err := tx.CreateBucketIfNotExists([]byte(bucketName))
		if err != nil {
			return err
		}

		// Marshal the list into JSON
		jsonData, err := json.Marshal(dataList)
		if err != nil {
			return err
		}

		// Save the data in the bucket
		err = bucket.Put([]byte("all"), jsonData) // Use a fixed key "all" to store the entire list
		return err
	})
	return err
}
