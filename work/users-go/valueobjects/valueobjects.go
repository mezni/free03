package valueobjects

import (
	"time"
)

type Limit struct {
	Limit     float64
	CreatedAt time.Time
	UpdatedAt time.Time
}
