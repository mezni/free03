package services

import (
    "encoding/json"
    "fmt"
    "io/ioutil"
    "os"

    "go.etcd.io/bbolt"
    "github.com/mezni/wovoka/cdrgen/application/dto"
    "github.com/mezni/wovoka/cdrgen/domain/entities"
)

// BaselineLoaderService defines the service for loading baseline data
type BaselineLoaderService struct {
    DB *bbolt.DB // bbolt instance to persist data
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
    if err = json.Unmarshal(byteValue, &data); err != nil {
        return fmt.Errorf("error unmarshaling data: %v", err)
    }

    // Process and save data for different types
    if err := b.processAndSave("NetworkTechnologies", data.NetworkTechnologies, b.processNetworkTechnologies); err != nil {
        return err
    }
    if err := b.processAndSave("NetworkElementTypes", data.NetworkElementTypes, b.processNetworkElementTypes); err != nil {
        return err
    }
    if err := b.processAndSave("ServiceTypes", data.ServiceTypes, b.processServiceTypes); err != nil {
        return err
    }

    return nil
}

// processAndSave is a generic function that processes and saves data to the database
func (b *BaselineLoaderService) processAndSave(bucketName string, dtoList interface{}, processFunc func(interface{}) (interface{}, error)) error {
    processedList, err := processFunc(dtoList)
    if err != nil {
        return fmt.Errorf("error processing %s: %v", bucketName, err)
    }
    if err := b.saveListToDB(bucketName, processedList); err != nil {
        return fmt.Errorf("error saving %s list: %v", bucketName, err)
    }
    return nil
}

// Process Network Technologies and return the list
func (b *BaselineLoaderService) processNetworkTechnologies(networkTechnologies interface{}) (interface{}, error) {
    ntList := networkTechnologies.([]dto.NetworkTechnologyDTO)
    var entitiesList []entities.NetworkTechnology
    for idseq, nt := range ntList {
        entitiesList = append(entitiesList, entities.NetworkTechnology{
            ID:          idseq + 1, // +1 because idseq should start from 1
            Name:        nt.Name,
            Description: nt.Description,
        })
    }
    return entitiesList, nil
}

// Process Network Element Types and return the list
func (b *BaselineLoaderService) processNetworkElementTypes(networkElementTypes interface{}) (interface{}, error) {
    netElementTypes := networkElementTypes.([]dto.NetworkElementTypeDTO)
    var entitiesList []entities.NetworkElementType
    for idseq, ne := range netElementTypes {
        entitiesList = append(entitiesList, entities.NetworkElementType{
            ID:                idseq + 1,
            Name:              ne.Name,
            Description:       ne.Description,
            NetworkTechnology: ne.NetworkTechnology,
        })
    }
    return entitiesList, nil
}

// Process Service Types and return the list
func (b *BaselineLoaderService) processServiceTypes(serviceTypes interface{}) (interface{}, error) {
    types := serviceTypes.([]dto.ServiceTypeDTO)
    var entitiesList []entities.ServiceType
    for idseq, st := range types {
        entitiesList = append(entitiesList, entities.ServiceType{
            ID:                idseq + 1,
            Name:              st.Name,
            Description:       st.Description,
            NetworkTechnology: st.NetworkTechnology,
        })
    }
    return entitiesList, nil
}

// Save a list of entities to the DB (using bbolt as an example)
func (b *BaselineLoaderService) saveListToDB(bucketName string, dataList interface{}) error {
    return b.DB.Update(func(tx *bbolt.Tx) error {
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
        return bucket.Put([]byte("all"), jsonData) // Use a fixed key "all" to store the entire list
    })
}