package valueobjects

import (
	"time"
)

type Limit struct {
	Amount    float64
	CreatedAt time.Time
	UpdatedAt time.Time
}
