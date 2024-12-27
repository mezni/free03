package services 

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os"

	"github.com/boltdb/bolt"
)

// BaselineLoaderService defines the service for loading baseline data
type BaselineLoaderService struct {
	DB *bolt.DB // BoltDB instance to persist data (you can swap with another DB)
}


func (b *BaselineLoaderService) LoadData(filename string) error {

}










package main

import (
    "fmt"
    "log"
    "os"

   
    "your_project_name/src/domain"
    "your_project_name/src/repository"
    "your_project_name/src/service"
    "your_project_name/src/utils"
)

// Function to save to the BoltDB
func saveToBoltDB(db *bolt.DB, bucketName string, key int, data interface{}) error {
    return db.Update(func(tx *bolt.Tx) error {
        bucket, err := tx.CreateBucketIfNotExists([]byte(bucketName))
        if err != nil {
            return err
        }
        jsonData, err := json.Marshal(data)
        if err != nil {
            return err
        }
        return bucket.Put([]byte(fmt.Sprintf("%d", key)), jsonData)
    })
}

func main() {
    // Open the BoltDB file
    db, err := bolt.Open("network_data.db", 0600, nil)
    if err != nil {
        log.Fatal(err)
    }
    defer db.Close()

    // Read the JSON file into a ConfigData struct
    var data struct {
        NetworkTechnology []domain.NetworkTechnologyDTO `json:"network_technology"`
        NetworkElements   []domain.NetworkElementDTO    `json:"network_elements"`
        ServiceTypes      []domain.ServiceTypeDTO       `json:"service_types"`
    }

    if err := utils.ReadJSONFile("data.json", &data); err != nil {
        log.Fatal(err)
    }

    // Initialize repositories
    ntRepo := &repository.InMemoryNetworkTechnologyRepository{}
    neRepo := &repository.InMemoryNetworkElementRepository{}
    stRepo := &repository.InMemoryServiceTypeRepository{}

    // Initialize services
    ntService := service.NewNetworkTechnologyService(ntRepo)
    neService := service.NewNetworkElementService(neRepo)
    stService := service.NewServiceTypeService(stRepo)

    // Assign IDs and save Network Technologies
    idseq := 1
    for _, ntDTO := range data.NetworkTechnology {
        nt := domain.NetworkTechnology{ID: idseq, Name: ntDTO.Name, Description: ntDTO.Description}
        if err := ntService.CreateNetworkTechnology(nt.Name, nt.Description); err != nil {
            log.Fatal(err)
        }
        if err := saveToBoltDB(db, "NetworkTechnologies", nt.ID, nt); err != nil {
            log.Fatal(err)
        }
        idseq++
    }

    // Reset ID sequence
    idseq = 1
    // Assign IDs and save Network Elements
    for _, neDTO := range data.NetworkElements {
        ne := domain.NetworkElement{ID: idseq, Name: neDTO.Name, Description: neDTO.Description, NetworkTechnology: neDTO.NetworkTechnology}
        if err := neService.CreateNetworkElement(ne.Name, ne.Description, ne.NetworkTechnology); err != nil {
            log.Fatal(err)
        }
        if err := saveToBoltDB(db, "NetworkElements", ne.ID, ne); err != nil {
            log.Fatal(err)
        }
        idseq++
    }

    // Reset ID sequence
    idseq = 1
    // Assign IDs and save Service Types
    for _, stDTO := range data.ServiceTypes {
        st := domain.ServiceType{ID: idseq, Name: stDTO.Name, Description: stDTO.Description, NetworkTechnology: stDTO.NetworkTechnology}
        if err := stService.CreateServiceType(st.Name, st.Description, st.NetworkTechnology); err != nil {
            log.Fatal(err)
        }
        if err := saveToBoltDB(db, "ServiceTypes", st.ID, st); err != nil {
            log.Fatal(err)
        }
        idseq++
    }

    fmt.Println("Data successfully loaded and saved.")
}