package entities

import (
	//	"github.com/google/uuid"
	"testing"
)

func TestNewUser(t *testing.T) {
	user := NewUser("dali")

	if user.Name != "dali" {
		t.Errorf("Expected product name to be 'dali', but got %s", user.Name)
	}

	err := user.validate()
	if err != nil {
		t.Fatalf("Expected no error, but got %s", err.Error())
	}

	err = user.UpdateName("dali1")
	if err != nil {
		t.Fatalf("Expected no error, but got %s", err.Error())
	}

}
