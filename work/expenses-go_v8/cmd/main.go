package main

import (
	"fmt"
	"github.com/google/uuid"
	"github.com/mezni/expenses-go/internal/domain/entities"
)

func main() {
	fmt.Println("- start")

	services := []map[string]string{
		{
			"provider": "aws",
			"service":  "ec2"},
		{
			"provider": "aws",
			"service":  "s3"},
	}

	for _, v := range services {
		providerID := uuid.New()
		s := entities.NewService(v["service"], providerID)

		fmt.Println(s)
	}
}
