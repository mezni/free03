package repositories

// CdrRepository defines the interface for interacting with CDR data.
type CdrRepository interface {
	Insert(cdr Cdr) error
	GetAll() ([]Cdr, error)
	GetByID(id int) (*Cdr, error)
	DeleteByID(id int) error
	GetFirstN(limit int) ([]Cdr, error)
	Length() (int, error)
}
