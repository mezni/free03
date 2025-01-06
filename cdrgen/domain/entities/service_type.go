package entities

type ServiceType struct {
	ID                int
	Name              string
	Description       string
	NetworkTechnology string
	BearerType        string
	JitterMin         int
	JitterMax         int
	LatencyMin        int
	LatencyMax        int
	ThroughputMin     int
	ThroughputMax     int
	PacketLossMin     float64
	PacketLossMax     float64
	CallSetupTimeMin  int
	CallSetupTimeMax  int
	MosMin            float64
	MosMax            float64
}
