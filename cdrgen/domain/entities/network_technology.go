package entities

type NetworkTechnology struct {
	ID          string
	Name        string
	Description string
}

var PredefinedNetworkTechnologies = map[string]NetworkTechnology{
  "2G": NetworkTechnology{ID: "2G", Name: "2G", Description: "GSM (Global System for Mobile Communications), CDMA (Code Division Multiple Access)"},
  "3G": NetworkTechnology{ID: "3G", Name: "3G", Description: "UMTS (Universal Mobile Telecommunications System), CDMA2000"},
  "4G": NetworkTechnology{ID: "4G", Name: "4G", Description: "LTE (Long-Term Evolution)"},
  "5G": NetworkTechnology{ID: "5G", Name: "5G", Description: "5G NR (New Radio)"},
}
