package sqlitestore

import (
	"database/sql"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"log"
)

// CustomerRepository handles database operations for customers.
type CustomerRepository struct {
	db *sql.DB
}

// NewCustomerRepository creates a new instance of CustomerRepository.
func NewCustomerRepository(db *sql.DB) *CustomerRepository {
	return &CustomerRepository{db: db}
}

// CreateTable creates the customers table with the required columns.
func (r *CustomerRepository) CreateTable() error {
	_, err := r.db.Exec(CreateCustomerTable)
	if err != nil {
		return fmt.Errorf("failed to create customers table: %w", err)
	}
	return nil
}

// Insert inserts a new customer into the database, but does not insert if the customer already exists.
func (r *CustomerRepository) Insert(customer entities.Customer) error {
	var existingID int
	err := r.db.QueryRow(SelectCustomerByMSISDN, customer.MSISDN).Scan(&existingID)
	if err == nil {
		log.Printf("Customer with MSISDN %s already exists, skipping insert.\n", customer.MSISDN)
		return nil
	}

	if err != sql.ErrNoRows {
		return fmt.Errorf("failed to check for existing customer: %w", err)
	}

	_, err = r.db.Exec(InsertCustomer, customer.MSISDN, customer.IMSI, customer.IMEI, customer.CustomerType, customer.AccountType, customer.Status)
	if err != nil {
		return fmt.Errorf("failed to insert customer: %w", err)
	}

	return nil
}

// GetAll retrieves all customers from the database.
func (r *CustomerRepository) GetAll() ([]entities.Customer, error) {
	rows, err := r.db.Query(SelectAllCustomers)
	if err != nil {
		return nil, fmt.Errorf("failed to query customers: %w", err)
	}
	defer rows.Close()

	var customers []entities.Customer
	for rows.Next() {
		var customer entities.Customer
		if err := rows.Scan(&customer.ID, &customer.MSISDN, &customer.IMSI, &customer.IMEI, &customer.CustomerType, &customer.AccountType, &customer.Status); err != nil {
			return nil, fmt.Errorf("failed to scan row into customer: %w", err)
		}
		customers = append(customers, customer)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("error occurred during row iteration: %w", err)
	}

	return customers, nil
}
