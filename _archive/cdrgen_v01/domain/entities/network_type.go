package entities

// NetworkType is a type that represents different network types.
type NetworkType int

// Constants for the available network types.
const (
	NetworkType2G NetworkType = iota
	NetworkType3G
	NetworkType4G
	NetworkType5G
)

// networkTypes is a list of available network types.
var networkTypes = []string{"2G", "3G", "4G", "5G"}

// String returns the string representation of the NetworkType.
func (nt NetworkType) String() string {
	if nt < NetworkType2G || nt > NetworkType5G {
		return "Unknown"
	}
	return networkTypes[nt]
}

// IsValidNetworkType checks if the given NetworkType is valid.
func IsValidNetworkType(networkType NetworkType) bool {
	return networkType >= NetworkType2G && networkType <= NetworkType5G
}