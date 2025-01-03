package interfaces

import (
	"encoding/json"
)

// Struct definitions as before
type NetworkTechnology struct {
	Name        string `json:"Name"`
	Description string `json:"Description"`
}

type NetworkElementType struct {
	Name              string `json:"Name"`
	Description       string `json:"Description"`
	NetworkTechnology string `json:"NetworkTechnology"`
}

type ServiceType struct {
	Name              string  `json:"Name"`
	Description       string  `json:"Description"`
	NetworkTechnology string  `json:"NetworkTechnology"`
	BearerType        string  `json:"BearerType"`
	JitterMin         float64 `json:"JitterMin"`
	JitterMax         float64 `json:"JitterMax"`
	LatencyMin        float64 `json:"LatencyMin"`
	LatencyMax        float64 `json:"LatencyMax"`
	ThroughputMin     float64 `json:"ThroughputMin"`
	ThroughputMax     float64 `json:"ThroughputMax"`
	PacketLossMin     float64 `json:"PacketLossMin"`
	PacketLossMax     float64 `json:"PacketLossMax"`
	CallSetupTimeMin  float64 `json:"CallSetupTimeMin"`
	CallSetupTimeMax  float64 `json:"CallSetupTimeMax"`
	MosMin            float64 `json:"MosMin"`
	MosMax            float64 `json:"MosMax"`
}

// New ServiceNode struct (No Nodes field in ServiceType now)
type ServiceNode struct {
	Name              string `json:"Name"`
	NetworkTechnology string `json:"NetworkTechnology"`
}

type Config struct {
	NetworkTechnologies []NetworkTechnology  `json:"network_technologies"`
	NetworkElementTypes []NetworkElementType `json:"network_element_types"`
	ServiceTypes        []ServiceType        `json:"service_types"`
	ServiceNodes        []ServiceNode        `json:"service_nodes"`
}

// Function to read JSON data and return the Config struct
func ReadConfig() (Config, error) {

	jsonData := []byte(`{
    "network_technologies": [
        {
            "Name": "2G",
            "Description": "2G"
        },
        {
            "Name": "3G",
            "Description": "3G"
        },
        {
            "Name": "4G",
            "Description": "4G"
        },
        {
            "Name": "5G",
            "Description": "5G"
        }
    ],
    "network_element_types": [
        {
            "Name": "BTS",
            "Description": "Base Transceiver Station: A base station responsible for radio communication with the mobile station.",
            "NetworkTechnology": "2G"
        },
        {
            "Name": "BSC",
            "Description": "Base Station Controller: Manages multiple BTS units, responsible for call setup and handovers.",
            "NetworkTechnology": "2G"
        },
        {
            "Name": "MSC",
            "Description": "Mobile Switching Center: Routes calls and manages connections in the mobile network.",
            "NetworkTechnology": "2G"
        },
        {
            "Name": "HLR",
            "Description": "Home Location Register: A central database that stores subscriber information and location.",
            "NetworkTechnology": "2G"
        },
        {
            "Name": "VLR",
            "Description": "Visitor Location Register: A temporary database that stores subscriber information for a specific location.",
            "NetworkTechnology": "2G"
        },
        {
            "Name": "AUC",
            "Description": "Authentication Center: Responsible for verifying subscriber identities.",
            "NetworkTechnology": "2G"
        },
        {
            "Name": "SMSC",
            "Description": "Short Message Service Center: Handles SMS delivery between users.",
            "NetworkTechnology": "2G"
        },
        {
            "Name": "GMSC",
            "Description": "Gateway MSC: Routes calls between mobile and other networks like PSTN.",
            "NetworkTechnology": "2G"
        },
        {
            "Name": "NodeB",
            "Description": "NodeB: The 3G base station responsible for radio communication.",
            "NetworkTechnology": "3G"
        },
        {
            "Name": "RNC",
            "Description": "Radio Network Controller: Manages NodeBs and controls radio access.",
            "NetworkTechnology": "3G"
        },
        {
            "Name": "MSC",
            "Description": "Mobile Switching Center: Routes calls and manages connections in the mobile network.",
            "NetworkTechnology": "3G"
        },
        {
            "Name": "SGSN",
            "Description": "Serving GPRS Support Node: Responsible for packet-switched data routing.",
            "NetworkTechnology": "3G"
        },
        {
            "Name": "GGSN",
            "Description": "Gateway GPRS Support Node: The node that connects the GPRS network to external data networks.",
            "NetworkTechnology": "3G"
        },
        {
            "Name": "HLR",
            "Description": "Home Location Register: Stores subscriber information.",
            "NetworkTechnology": "3G"
        },
        {
            "Name": "VLR",
            "Description": "Visitor Location Register: Temporarily stores subscriber data when they roam.",
            "NetworkTechnology": "3G"
        },
        {
            "Name": "CGF",
            "Description": "Charging Gateway Function: Handles billing and charging for network usage.",
            "NetworkTechnology": "3G"
        },
        {
            "Name": "SMSC",
            "Description": "Short Message Service Center: Manages SMS delivery.",
            "NetworkTechnology": "3G"
        },
        {
            "Name": "PCRF",
            "Description": "Policy and Charging Rules Function: Determines user policies and charging.",
            "NetworkTechnology": "3G"
        },
        {
            "Name": "IMS",
            "Description": "The IMS (IP Multimedia Subsystem) is a core network element in modern mobile networks.",
            "NetworkTechnology": "3G"
        },
        {
            "Name": "eNodeB",
            "Description": "Evolved NodeB: The base station in 4G LTE, responsible for radio access.",
            "NetworkTechnology": "4G"
        },
        {
            "Name": "EPC",
            "Description": "Evolved Packet Core: The core network architecture for 4G LTE, handling both data and voice services.",
            "NetworkTechnology": "4G"
        },
        {
            "Name": "SGW",
            "Description": "Serving Gateway: Routes data from the eNodeB to the external network.",
            "NetworkTechnology": "4G"
        },
        {
            "Name": "PGW",
            "Description": "PDN Gateway: Provides connectivity between the LTE network and external IP networks.",
            "NetworkTechnology": "4G"
        },
        {
            "Name": "MME",
            "Description": "Mobility Management Entity: Manages mobility and session control for 4G networks.",
            "NetworkTechnology": "4G"
        },
        {
            "Name": "HSS",
            "Description": "Home Subscriber Server: Stores user profile and authentication data.",
            "NetworkTechnology": "4G"
        },
        {
            "Name": "PCRF",
            "Description": "Policy and Charging Rules Function: Manages quality of service and charging policies.",
            "NetworkTechnology": "4G"
        },
        {
            "Name": "SMSC",
            "Description": "Short Message Service Center: Manages SMS delivery.",
            "NetworkTechnology": "4G"
        },
        {
            "Name": "VoLTE Gateway",
            "Description": "Voice over LTE Gateway: Facilitates voice communication over the LTE network.",
            "NetworkTechnology": "4G"
        },
        {
            "Name": "IMS",
            "Description": "The IMS (IP Multimedia Subsystem) is a core network element in modern mobile networks.",
            "NetworkTechnology": "4G"
        },
        {
            "Name": "gNodeB",
            "Description": "gNodeB: The 5G base station responsible for providing radio access.",
            "NetworkTechnology": "5G"
        },
        {
            "Name": "AMF",
            "Description": "Access and Mobility Management Function: Handles the registration, mobility, and security of users in 5G.",
            "NetworkTechnology": "5G"
        },
        {
            "Name": "SMF",
            "Description": "Session Management Function: Manages the session state in 5G networks.",
            "NetworkTechnology": "5G"
        },
        {
            "Name": "UPF",
            "Description": "User Plane Function: Handles data packet forwarding and routing in 5G.",
            "NetworkTechnology": "5G"
        },
        {
            "Name": "PCF",
            "Description": "Policy Control Function: Manages quality of service and charging policies in 5G networks.",
            "NetworkTechnology": "5G"
        },
        {
            "Name": "UDM",
            "Description": "Unified Data Management: Stores subscription data for users.",
            "NetworkTechnology": "5G"
        },
        {
            "Name": "NRF",
            "Description": "Network Repository Function: Maintains a repository of available network functions and their capabilities.",
            "NetworkTechnology": "5G"
        },
        {
            "Name": "NSSF",
            "Description": "Network Slice Selection Function: Assigns network slices to users based on their subscription and needs.",
            "NetworkTechnology": "5G"
        },
        {
            "Name": "AUSF",
            "Description": "Authentication Server Function: Performs user authentication in 5G networks.",
            "NetworkTechnology": "5G"
        },
        {
            "Name": "IMS",
            "Description": "The IMS (IP Multimedia Subsystem) is a core network element in modern mobile networks, including 5G.",
            "NetworkTechnology": "5G"
        },
        {
            "Name": "NEF",
            "Description": "Network Exposure Function: Provides secure and standardized APIs for external applications to access 5G network functions.",
            "NetworkTechnology": "5G"
        },
        {
            "Name": "AF",
            "Description": "Application Function: Interfaces with the 5G core to provide application-specific services.",
            "NetworkTechnology": "5G"
        }
    ],
    "service_types": [
        {
            "Name": "Voice Call",
            "NetworkTechnology": "2G",
            "BearerType": "Circuit-Switched",
            "JitterMin": 0,
            "JitterMax": 5,
            "LatencyMin": 100,
            "LatencyMax": 500,
            "ThroughputMin": 10,
            "ThroughputMax": 100,
            "PacketLossMin": 0,
            "PacketLossMax": 2,
            "CallSetupTimeMin": 1000,
            "CallSetupTimeMax": 3000,
            "MosMin": 3,
            "MosMax": 3.5
        },
        {
            "Name": "SMS",
            "NetworkTechnology": "2G",
            "BearerType": "Circuit-Switched",
            "JitterMin": 0,
            "JitterMax": 5,
            "LatencyMin": 100,
            "LatencyMax": 500,
            "ThroughputMin": 10,
            "ThroughputMax": 100,
            "PacketLossMin": 0,
            "PacketLossMax": 2,
            "CallSetupTimeMin": 1000,
            "CallSetupTimeMax": 3000,
            "MosMin": 3,
            "MosMax": 3.5
        },
        {
            "Name": "MMS",
            "NetworkTechnology": "2G",
            "BearerType": "Circuit-Switched",
            "JitterMin": 0,
            "JitterMax": 5,
            "LatencyMin": 100,
            "LatencyMax": 500,
            "ThroughputMin": 10,
            "ThroughputMax": 100,
            "PacketLossMin": 0,
            "PacketLossMax": 2,
            "CallSetupTimeMin": 1000,
            "CallSetupTimeMax": 3000,
            "MosMin": 3,
            "MosMax": 3.5
        },
        {
            "Name": "Voice Call",
            "NetworkTechnology": "3G",
            "BearerType": "Circuit-Switched",
            "JitterMin": 5,
            "JitterMax": 20,
            "LatencyMin": 50,
            "LatencyMax": 200,
            "ThroughputMin": 100,
            "ThroughputMax": 500,
            "PacketLossMin": 0,
            "PacketLossMax": 1,
            "CallSetupTimeMin": 500,
            "CallSetupTimeMax": 1500,
            "MosMin": 3.5,
            "MosMax": 4
        },
        {
            "Name": "SMS",
            "NetworkTechnology": "3G",
            "BearerType": "Circuit-Switched",
            "JitterMin": 5,
            "JitterMax": 20,
            "LatencyMin": 50,
            "LatencyMax": 200,
            "ThroughputMin": 100,
            "ThroughputMax": 500,
            "PacketLossMin": 0,
            "PacketLossMax": 1,
            "CallSetupTimeMin": 500,
            "CallSetupTimeMax": 1500,
            "MosMin": 3.5,
            "MosMax": 4
        },
        {
            "Name": "Data",
            "NetworkTechnology": "3G",
            "BearerType": "Packet-Switched",
            "JitterMin": 5,
            "JitterMax": 20,
            "LatencyMin": 50,
            "LatencyMax": 200,
            "ThroughputMin": 100,
            "ThroughputMax": 500,
            "PacketLossMin": 0,
            "PacketLossMax": 1,
            "CallSetupTimeMin": 500,
            "CallSetupTimeMax": 1500,
            "MosMin": 3.5,
            "MosMax": 4
        },
        {
            "Name": "Voice Call",
            "NetworkTechnology": "4G",
            "BearerType": "VoLTE",
            "JitterMin": 2,
            "JitterMax": 10,
            "LatencyMin": 10,
            "LatencyMax": 50,
            "ThroughputMin": 500,
            "ThroughputMax": 1000,
            "PacketLossMin": 0,
            "PacketLossMax": 0.5,
            "CallSetupTimeMin": 300,
            "CallSetupTimeMax": 1000,
            "MosMin": 4,
            "MosMax": 4.5
        },
        {
            "Name": "SMS",
            "NetworkTechnology": "4G",
            "BearerType": "IMS",
            "JitterMin": 2,
            "JitterMax": 10,
            "LatencyMin": 10,
            "LatencyMax": 50,
            "ThroughputMin": 500,
            "ThroughputMax": 1000,
            "PacketLossMin": 0,
            "PacketLossMax": 0.5,
            "CallSetupTimeMin": 300,
            "CallSetupTimeMax": 1000,
            "MosMin": 4,
            "MosMax": 4.5
        },
        {
            "Name": "Data",
            "NetworkTechnology": "4G",
            "BearerType": "Packet-Switched",
            "JitterMin": 2,
            "JitterMax": 10,
            "LatencyMin": 10,
            "LatencyMax": 50,
            "ThroughputMin": 1000,
            "ThroughputMax": 5000,
            "PacketLossMin": 0,
            "PacketLossMax": 0.5,
            "CallSetupTimeMin": 300,
            "CallSetupTimeMax": 1000,
            "MosMin": 4,
            "MosMax": 4.5
        },
        {
            "Name": "Voice Call",
            "NetworkTechnology": "5G",
            "BearerType": "VoNR",
            "JitterMin": 1,
            "JitterMax": 5,
            "LatencyMin": 1,
            "LatencyMax": 20,
            "ThroughputMin": 1000,
            "ThroughputMax": 10000,
            "PacketLossMin": 0,
            "PacketLossMax": 0.2,
            "CallSetupTimeMin": 100,
            "CallSetupTimeMax": 500,
            "MosMin": 4.5,
            "MosMax": 5
        },
        {
            "Name": "SMS",
            "NetworkTechnology": "5G",
            "BearerType": "IMS",
            "JitterMin": 1,
            "JitterMax": 5,
            "LatencyMin": 1,
            "LatencyMax": 20,
            "ThroughputMin": 1000,
            "ThroughputMax": 10000,
            "PacketLossMin": 0,
            "PacketLossMax": 0.2,
            "CallSetupTimeMin": 100,
            "CallSetupTimeMax": 500,
            "MosMin": 4.5,
            "MosMax": 5
        },
        {
            "Name": "Data",
            "NetworkTechnology": "5G",
            "BearerType": "Packet-Switched",
            "JitterMin": 1,
            "JitterMax": 5,
            "LatencyMin": 1,
            "LatencyMax": 20,
            "ThroughputMin": 1000,
            "ThroughputMax": 10000,
            "PacketLossMin": 0,
            "PacketLossMax": 0.2,
            "CallSetupTimeMin": 100,
            "CallSetupTimeMax": 500,
            "MosMin": 4.5,
            "MosMax": 5
        },
        {
            "Name": "Video Call",
            "NetworkTechnology": "4G",
            "BearerType": "VoLTE",
            "JitterMin": 2,
            "JitterMax": 10,
            "LatencyMin": 10,
            "LatencyMax": 50,
            "ThroughputMin": 500,
            "ThroughputMax": 1000,
            "PacketLossMin": 0,
            "PacketLossMax": 0.5,
            "CallSetupTimeMin": 300,
            "CallSetupTimeMax": 1000,
            "MosMin": 4,
            "MosMax": 4.5
        },
        {
            "Name": "Video Call",
            "NetworkTechnology": "5G",
            "BearerType": "VoNR",
            "JitterMin": 1,
            "JitterMax": 5,
            "LatencyMin": 1,
            "LatencyMax": 20,
            "ThroughputMin": 1000,
            "ThroughputMax": 10000,
            "PacketLossMin": 0,
            "PacketLossMax": 0.2,
            "CallSetupTimeMin": 100,
            "CallSetupTimeMax": 500,
            "MosMin": 4.5,
            "MosMax": 5
        }
    ],
    "service_nodes": [
        {
            "Name": "Voice Call",
            "NetworkTechnology": "2G",
            "Nodes": "MSC"
        },
        {
            "Name": "SMS",
            "NetworkTechnology": "2G",
            "Nodes": "SMSC"
        },
        {
            "Name": "MMS",
            "NetworkTechnology": "2G",
            "Nodes": "MMSC"
        },
        {
            "Name": "Voice Call",
            "NetworkTechnology": "3G",
            "Nodes": "RNC, MSC"
        },
        {
            "Name": "SMS",
            "NetworkTechnology": "3G",
            "Nodes": "SMSC"
        },
        {
            "Name": "Data",
            "NetworkTechnology": "3G",
            "Nodes": "RNC, GGSN"
        },
        {
            "Name": "Voice Call",
            "NetworkTechnology": "4G",
            "Nodes": "IMS"
        },
        {
            "Name": "SMS",
            "NetworkTechnology": "4G",
            "Nodes": "SMSC, IMS"
        },
        {
            "Name": "Data",
            "NetworkTechnology": "4G",
            "Nodes": "IMS, PGW"
        },
        {
            "Name": "Voice Call",
            "NetworkTechnology": "5G",
            "Nodes": "gNodeB"
        },
        {
            "Name": "SMS",
            "NetworkTechnology": "5G",
            "Nodes": "SMSC, gNodeB"
        },
        {
            "Name": "Data",
            "NetworkTechnology": "5G",
            "Nodes": "gNodeB, UPF"
        },
        {
            "Name": "Video Call",
            "NetworkTechnology": "4G",
            "Nodes": "IMS"
        },
        {
            "Name": "Video Call",
            "NetworkTechnology": "5G",
            "Nodes": "gNodeB"
        }
    ]
}`)

	var config Config
	err := json.Unmarshal(jsonData, &config)
	if err != nil {
		return config, err
	}
	return config, nil
}
