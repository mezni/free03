package main

import (
	"fmt"
	"github.com/google/uuid"
	"time"
)

type Period struct {
	ID        uuid.UUID
	Code      string
	Date      time.Time
	Year      int
	Quarter   int
	Month     int
	Week      int
	Day       int
	DayOfWeek int
	DayOfYear int
	IsWeekend bool
	IsHoliday bool
}

func NewPeriod(code string) (*Period, error) {
	layout := "2006-01-02"

	date, err := time.Parse(layout, code)
	if err != nil {
		return nil, err
	}

	year, week := date.ISOWeek()

	return &Period{
		ID:        uuid.New(),
		Code:      code,
		Date:      date,
		Year:      year,
		Quarter:   int((date.Month()-1)/3) + 1,
		Month:     int(date.Month()),
		Week:      week,
		Day:       date.Day(),
		DayOfWeek: int(date.Weekday()),
		DayOfYear: date.YearDay(),
		IsWeekend: date.Weekday() == 6 && date.Weekday() == 7,
		IsHoliday: false,
	}, nil
}

func main() {
	fmt.Println("- start")
	period, _ := NewPeriod("2024-05-30")
	fmt.Println(period)
}
