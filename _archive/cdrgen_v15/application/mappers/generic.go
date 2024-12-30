package mappers

import (
	"errors"
	"fmt"
	"reflect"
	"strconv"
)

// Error definitions
var (
	ErrMissingField    = errors.New("missing required field in the map")
	ErrInvalidID       = errors.New("invalid ID, must be a positive integer")
	ErrConversionID    = errors.New("unable to convert ID to an integer")
)

// Mapper provides generic mapping functionality for entities.
type Mapper[T any] struct {
	EntityType reflect.Type
}

// NewMapper creates a new Mapper for a given entity type.
func NewMapper[T any]() *Mapper[T] {
	var entity T
	return &Mapper[T]{
		EntityType: reflect.TypeOf(entity),
	}
}

// ToMap converts an entity to a map, with ID as a string.
func (m *Mapper[T]) ToMap(entity T) (map[string]interface{}, error) {
	result := make(map[string]interface{})
	
	val := reflect.ValueOf(entity)
	if val.Kind() == reflect.Ptr {
		val = val.Elem()
	}

	if val.Kind() != reflect.Struct {
		return nil, fmt.Errorf("expected a struct, got %s", val.Kind())
	}

	for i := 0; i < val.NumField(); i++ {
		field := val.Type().Field(i)
		fieldName := field.Name
		fieldValue := val.Field(i).Interface()

		if fieldName == "ID" {
			if id, ok := fieldValue.(int); ok {
				result[fieldName] = strconv.Itoa(id) // Convert ID to string
			} else {
				return nil, ErrInvalidID
			}
		} else {
			result[fieldName] = fieldValue
		}
	}

	return result, nil
}

// FromMap converts a map to an entity, with ID as an integer.
func (m *Mapper[T]) FromMap(data map[string]interface{}) (T, error) {
	var entity T
	val := reflect.ValueOf(&entity).Elem()

	if val.Kind() != reflect.Struct {
		return entity, fmt.Errorf("expected a struct, got %s", val.Kind())
	}

	for i := 0; i < val.NumField(); i++ {
		field := val.Type().Field(i)
		fieldName := field.Name
		fieldValue, ok := data[fieldName]
		if !ok {
			return entity, fmt.Errorf("%w: %s", ErrMissingField, fieldName)
		}

		if fieldName == "ID" {
			switch v := fieldValue.(type) {
			case string:
				parsedID, err := strconv.Atoi(v)
				if err != nil {
					return entity, ErrConversionID
				}
				if parsedID <= 0 {
					return entity, ErrInvalidID
				}
				val.Field(i).SetInt(int64(parsedID))
			case int:
				if v <= 0 {
					return entity, ErrInvalidID
				}
				val.Field(i).SetInt(int64(v))
			default:
				return entity, ErrInvalidID
			}
		} else {
			val.Field(i).Set(reflect.ValueOf(fieldValue))
		}
	}

	return entity, nil
}

// ToListMap converts a slice of entities to a slice of maps.
func (m *Mapper[T]) ToListMap(entities []T) ([]map[string]interface{}, error) {
	var result []map[string]interface{}
	for _, entity := range entities {
		mapped, err := m.ToMap(entity)
		if err != nil {
			return nil, err
		}
		result = append(result, mapped)
	}
	return result, nil
}

// FromListMap converts a slice of maps to a slice of entities.
func (m *Mapper[T]) FromListMap(data []map[string]interface{}) ([]T, error) {
	var result []T
	for _, item := range data {
		entity, err := m.FromMap(item)
		if err != nil {
			return nil, err
		}
		result = append(result, entity)
	}
	return result, nil
}