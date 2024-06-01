package domain

type ExpenseRepository interface {
	GetByID(id int) (*Expense, error)
	Create(expense *Expense) error
}
