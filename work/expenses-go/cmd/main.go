package main

import (
	"fmt"
)

func main() {
	fmt.Println("- start")

	e := []map[string]string{
		{
			"provider": "aws",
			"service":  "ec2"},
		{
			"provider": "aws",
			"service":  "s3"},
	}
	fmt.Println(e)
}
