package logic

import (
	"strings"
)

// MockDatabase is a mock in-memory implementation of the Database interface,
// useful for testing logic without setting up a real database.
type MockDatabase struct {
	products map[string]Product
}

// NewMockDatabase is the way to initialize a MockDatabase.
func NewMockDatabase() *MockDatabase {
	return &MockDatabase{products: make(map[string]Product)}
}

func (m *MockDatabase) CreateProduct(product Product) error {
	if _, exists := m.products[product.ID]; exists {
		return ErrDuplicateProductID
	}
	m.products[product.ID] = product
	return nil
}

func (m *MockDatabase) GetProduct(id string) (Product, error) {
	product, exists := m.products[id]
	if !exists {
		return Product{}, ErrProductNotFound
	}
	return product, nil
}

func (m *MockDatabase) SearchProducts(query string) ([]Product, error) {
	var results []Product
	for _, product := range m.products {
		if strings.Contains(strings.ToLower(product.Name), strings.ToLower(query)) {
			results = append(results, product)
		}
	}
	return results, nil
}

func (m *MockDatabase) UpdateProduct(product Product) error {
	if _, exists := m.products[product.ID]; !exists {
		return ErrProductNotFound
	}
	m.products[product.ID] = product
	return nil
}
