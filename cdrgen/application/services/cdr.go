package service

import (
	"errors"
	"fmt"
	"sync"
	"time"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// CDRRepository defines the interface for interacting with the CDR storage.
type CDRRepository interface {
	Save(cdr entities.CDR) error
	FindByID(id string) (entities.CDR, error)
	FindAll() ([]entities.CDR, error)
}

// CDRService provides business logic for managing CDRs.
type CDRService struct {
	sequence  int64 // A counter for creating sequential IDs, initialized with UnixNano timestamp
	repository CDRRepository
	mu         sync.Mutex
}

// NewCDRService creates a new instance of CDRService.
func NewCDRService(repository CDRRepository) *CDRService {
	// Initialize sequence with the current timestamp in nanoseconds
	return &CDRService{
		repository: repository,
		sequence:   time.Now().UnixNano(), // Set the initial sequence to Unix timestamp in nanoseconds
	}
}

// generateUniqueID generates a unique ID based on the sequence (Unix timestamp).
func (s *CDRService) generateUniqueID() string {
	s.mu.Lock()
	defer s.mu.Unlock()

	// Increment the sequence
	s.sequence++

	// Return a unique ID combining the sequence (Unix timestamp)
	return fmt.Sprintf("CDR-%d", s.sequence)
}

// CreateCDR generates a new CDR with the provided data.
func (s *CDRService) CreateCDR(cdrID string) (entities.CDR, error) {
	if cdrID == "" {
		return entities.CDR{}, errors.New("cdrID cannot be empty")
	}

	cdr := entities.CDR{
		ID:        s.generateUniqueID(),
		CdrID:     cdrID,
		Timestamp: time.Now(),
	}

	// Save the CDR to the repository
	err := s.repository.Save(cdr)
	if err != nil {
		return entities.CDR{}, err
	}

	return cdr, nil
}
