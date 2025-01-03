package entities

// ServiceType represents the service type entity.
type ServiceType struct {
	ID                int
	Name              string
	Description       string
	NetworkTechnology string
	Nodes             []string  
	BearerType        string   
	JitterMin       int   
	JitterMax      int      
	LatencyMin      int     
	LatencyMax     int   
	ThroughputMin   int  
	ThroughputMax   int    
	PacketLossMin   int
	PacketLossMax   int      
	CallSetupTimeMin int  
	CallSetupTimeMax int      
	MosRangeMin          float64 
	MosRangeMax          float64 
}