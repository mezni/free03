package queries

import (
	"github.com/google/uuid"
	"github.com/mezni/expenses-go/internal/application/commons"
)

type OrgQueryResult struct {
	Result *commons.OrgResult
}

type OrgQueryListResult struct {
	Result []*commons.OrgResult
}
