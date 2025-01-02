package services

import (
	"encoding/json"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
	"io/ioutil"
)

type ConfigLoaderService struct {
	NetworkTechnologyRepo  sqlitestore.NetworkTechnologyRepository
	NetworkElementTypeRepo sqlitestore.NetworkElementTypeRepository
	ServiceTypeRepo        sqlitestore.ServiceTypeRepository
}

func NewConfigLoaderService(
	networkTechnologyRepo sqlitestore.NetworkTechnologyRepository,
	networkElementTypeRepo sqlitestore.NetworkElementTypeRepository,
	serviceTypeRepo sqlitestore.ServiceTypeRepository) *ConfigLoaderService {

	return &ConfigLoaderService{
		NetworkTechnologyRepo:  networkTechnologyRepo,
		NetworkElementTypeRepo: networkElementTypeRepo,
		ServiceTypeRepo:        serviceTypeRepo,
	}
}
