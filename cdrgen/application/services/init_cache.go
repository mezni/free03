package services

type InitCacheService struct {
	configFile string
	dbFile     string
}

func NewInitCacheService(configFile, dbFile string) *InitCacheService {
	return &InitCacheService{
		configFile: configFile,
		dbFile:     dbFile,
	}
}

func (s *InitCacheService) InitializeCache() error {
	return nil
}
