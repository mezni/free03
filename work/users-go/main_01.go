package main

import (
	"fmt"
)

type InputData struct {
	Name   string
	Limit  float64
	Parent string
}

func main() {

	data := []InputData{
		InputData{Name: "default", Limit: 0, Parent: ""},
		InputData{Name: "IT", Limit: 0, Parent: "default"},
	}
	fmt.Println("- start")
	for _, k := range data {
		fmt.Println(k)
	}
	fmt.Println("- end")
}
