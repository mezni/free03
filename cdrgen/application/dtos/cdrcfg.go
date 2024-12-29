package dtos

type CfgData struct {
	Locations struct {
		Latitude      []float64 `yaml:"Latitude"`
		Longitude     []float64 `yaml:"Longitude"`
		LocationSplit []struct {
			NetworkTechnology string   `yaml:"NetworkTechnology"`
			SplitRows         int      `yaml:"SplitRows"`
			SplitColumns      int      `yaml:"SplitColumns"`
			LocationNames     []string `yaml:"LocationNames"`
		} `yaml:"LocationSplit"`
	} `yaml:"Locations"`
}
