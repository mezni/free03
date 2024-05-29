package main

import (
	"fmt"
	"github.com/google/uuid"
)

type Portfolio struct {
	ID            uuid.UUID
	Name          string
	PortfolioType string
	Limit         float64
	Parent        *uuid.UUID
}

func NewPortfolio(name string, portfolioType string, limit float64, parent *uuid.UUID) (*Portfolio, error) {
	return &Portfolio{ID: uuid.New(), Name: name, PortfolioType: portfolioType, Limit: limit, Parent: parent}, nil
}

type PortfolioInput struct {
	Name          string
	PortfolioType string
	Limit         float64
	Parent        string
}

func generate() []*Portfolio {
	var portfolios []*Portfolio
	portfolioInput := []PortfolioInput{
		{"root", "default", 3000, ""},
		{"IT", "department", 2000, "root"},
		{"HR", "department", 500, "root"},
		{"Sales", "department", 500, "root"},
		{"team1", "team", 1000, "IT"},
		{"team2", "team", 500, "IT"},
		{"phonix1", "project", 500, "IT"},
		{"phonix2", "project", 500, "IT"},
		{"hr1", "project", 300, "IT"},
	}
	for _, v := range portfolioInput {
		if v.Parent == "" {
			p, _ := NewPortfolio(v.Name, v.PortfolioType, v.Limit, nil)
			portfolios = append(portfolios, p)
		} else {
			for _, p := range portfolios {
				if v.Parent == p.Name {
					parentID := p.ID
					p, _ := NewPortfolio(v.Name, v.PortfolioType, v.Limit, &parentID)
					portfolios = append(portfolios, p)
					break
				}
			}
		}
	}
	//	for _, p := range portfolios {
	//		fmt.Println(p.ID, p.Name, p.PortfolioType, p.Limit, p.Parent)
	//	}
	return portfolios
}

func test3(portfolios []*Portfolio) {
	uuids := make([]*uuid.UUID, 0)
	children_uuids := make([]*uuid.UUID, 0)
	for _, p := range portfolios {
		if p.Parent == nil {
			uuids = append(uuids, nil)
			children_uuids = append(children_uuids, &p.ID)
		}
	}

	for len(children_uuids) > 0 {
		fmt.Println(uuids)
		fmt.Println(children_uuids)
		uuids = children_uuids
		children_uuids = []*uuid.UUID{}
		for _, p := range portfolios {
			for _, v := range uuids {
				if p.Parent != nil {
					if p.Parent.String() == v.String() {
						//					fmt.Println(p.ID, p.Name, p.PortfolioType, p.Limit, p.Parent)
						children_uuids = append(children_uuids, &p.ID)
					}
				}
			}
		}
	}
}

func getChildren(portfolios []*Portfolio, uuids []*uuid.UUID) []*uuid.UUID {
	children_uuids := make([]*uuid.UUID, 0)
	if len(uuids) == 0 {
		for _, p := range portfolios {
			if p.Parent == nil {
				children_uuids = append(children_uuids, &p.ID)
			}
		}
	} else {
		for _, p := range portfolios {
			for _, v := range uuids {
				if p.Parent != nil && p.Parent.String() == v.String() {
					children_uuids = append(children_uuids, &p.ID)
				}
			}
		}
	}

	return children_uuids
}
func processLevel(children_uuids []*uuid.UUID) {
	fmt.Println(children_uuids)
}

func test4(portfolios []*Portfolio) {
	uuids := make([]*uuid.UUID, 0)

	children_uuids := getChildren(portfolios, uuids)
	for len(children_uuids) > 0 {
		processLevel(children_uuids)
		uuids = children_uuids
		children_uuids = getChildren(portfolios, uuids)
	}

}

func main() {
	fmt.Println("- start")
	portfolios := generate()
	test4(portfolios)

}
