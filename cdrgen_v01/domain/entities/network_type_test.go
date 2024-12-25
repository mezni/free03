package entities

import (
	"testing"
)

func TestNetworkTypeString(t *testing.T) {
	tests := []struct {
		networkType NetworkType
		expected    string
	}{
		{NetworkType2G, "2G"},
		{NetworkType3G, "3G"},
		{NetworkType4G, "4G"},
		{NetworkType5G, "5G"},
		{NetworkType(999), "Unknown"}, // Testing invalid NetworkType
	}

	for _, test := range tests {
		t.Run(test.expected, func(t *testing.T) {
			result := test.networkType.String()
			if result != test.expected {
				t.Errorf("expected %v, got %v", test.expected, result)
			}
		})
	}
}

func TestIsValidNetworkType(t *testing.T) {
	tests := []struct {
		networkType NetworkType
		expected    bool
	}{
		{NetworkType2G, true},
		{NetworkType3G, true},
		{NetworkType4G, true},
		{NetworkType5G, true},
		{NetworkType(999), false}, // Invalid NetworkType
	}

	for _, test := range tests {
		t.Run(test.networkType.String(), func(t *testing.T) {
			result := IsValidNetworkType(test.networkType)
			if result != test.expected {
				t.Errorf("expected %v, got %v", test.expected, result)
			}
		})
	}
}
