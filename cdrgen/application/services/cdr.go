package application

import (
	"errors"
	"time"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

type CDRService struct {
	cdrRepositories       []domain.CDRRepository
	customerRepository    domain.CustomerRepository
	networkElementRepo    domain.NetworkElementRepository
}

func NewCDRService(
	cdrRepositories []domain.CDRRepository,
	customerRepo domain.CustomerRepository,
	networkElementRepo domain.NetworkElementRepository,
) *CDRService {
	return &CDRService{
		cdrRepositories:    cdrRepositories,
		customerRepository: customerRepo,
		networkElementRepo: networkElementRepo,
	}
}

func (s *CDRService) GenerateRandomCDR(callType string, duration int) (domain.CDR, error) {
	if duration <= 0 {
		return domain.CDR{}, errors.New("invalid call duration")
	}

	caller, err := s.customerRepository.FindRandom()
	if err != nil {
		return domain.CDR{}, errors.New("failed to find caller: " + err.Error())
	}

	callee, err := s.customerRepository.FindRandom()
	if err != nil {
		return domain.CDR{}, errors.New("failed to find callee: " + err.Error())
	}

	for caller.MSISDN == callee.MSISDN {
		callee, err = s.customerRepository.FindRandom()
		if err != nil {
			return domain.CDR{}, errors.New("failed to find unique callee: " + err.Error())
		}
	}

	networkElement, err := s.networkElementRepo.FindRandom()
	if err != nil {
		return domain.CDR{}, errors.New("failed to find network element: " + err.Error())
	}

	cdr := domain.CDR{
		ID:        generateUniqueID(),
		Caller:    caller.MSISDN,
		Callee:    callee.MSISDN,
		Duration:  duration,
		Timestamp: time.Now(),
		CallType:  callType + " via " + networkElement.Name,
	}

	for _, repo := range s.cdrRepositories {
		if err := repo.Save(cdr); err != nil {
			return domain.CDR{}, err
		}
	}

	return cdr, nil
}

// Mock implementation for unique ID generation
func generateUniqueID() string {
	return fmt.Sprintf("CDR-%d", time.Now().UnixNano())
}
