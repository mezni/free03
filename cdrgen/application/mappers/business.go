package mappers

// BusinessConfig represents the configuration read from the YAML file.
type BusinessConfig struct {
	Country     string `yaml:"Country"`
	Coordinates struct {
		Latitude  [2]float64 `yaml:"latitude"`
		Longitude [2]float64 `yaml:"longitude"`
	} `yaml:"Coordinates"`

	// Networks is now a map where the key is the network type (e.g., "2G", "3G", "4G")
	Networks map[string]struct {
		Rows          int      `yaml:"Rows"`
		Columns       int      `yaml:"Columns"`
		LocationNames []string `yaml:"LocationNames"`
	} `yaml:"Networks"`

	// Customer information
	Customer struct {
		Msisdn struct {
			Home struct {
				CountryCode string   `yaml:"country_code"`
				NdcRanges   [][2]int `yaml:"ndc_ranges"`
				Digits      int      `yaml:"digits"`
				Count       int      `yaml:"count"`
			} `yaml:"home"`
			National struct {
				CountryCode string   `yaml:"country_code"`
				NdcRanges   [][2]int `yaml:"ndc_ranges"`
				Digits      int      `yaml:"digits"`
				Count       int      `yaml:"count"`
			} `yaml:"national"`
			International struct {
				Prefixes []string `yaml:"prefixes"`
				Digits   int      `yaml:"digits"`
				Count    int      `yaml:"count"`
			} `yaml:"international"`
		} `yaml:"msisdn"`
	} `yaml:"customer"`
}
