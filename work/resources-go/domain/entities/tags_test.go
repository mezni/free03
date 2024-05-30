package entities



import (
//	"github.com/google/uuid"
	"testing"
)

func TestNewTag(t *testing.T) {
    tag:=NewTag("cloud", "key", "value")
	if tag.Key != "key" {
		t.Errorf("Expected tag key to be 'key', but got %s", tag.Key)
	}    

}