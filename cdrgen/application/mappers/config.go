package mappers

type Config struct {
	Country     string `yaml:"country"`
	Coordinates struct {
		Latitude  [2]float64 `yaml:"latitude"`
		Longitude [2]float64 `yaml:"longitude"`
	} `yaml:"coordinates"`
	Networks map[string]struct {
		Rows          int      `yaml:"rows"`
		Columns       int      `yaml:"columns"`
		LocationNames []string `yaml:"location_names"`
	} `yaml:"networks"`
}
