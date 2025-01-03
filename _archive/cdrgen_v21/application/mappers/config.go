package mappers

type Config struct {
	Country     string `yaml:"Country"`
	Coordinates struct {
		Latitude  [2]float64 `yaml:"latitude"`
		Longitude [2]float64 `yaml:"longitude"`
	} `yaml:"Coordinates"`
	Networks map[string]struct {
		Rows          int      `yaml:"Rows"`
		Columns       int      `yaml:"Columns"`
		LocationNames []string `yaml:"LocationNames"`
	} `yaml:"Networks"`
}
