package logic

import (
	"strings"

	"github.com/daominah/gostructure/pkg/model"
)

// MockDatabase is a mock in-memory implementation of the Database interface,
// useful for testing logic without setting up a real database.
type MockDatabase struct {
	products map[string]model.Product
}

// NewMockDatabase is the way to initialize a MockDatabase.
func NewMockDatabase() *MockDatabase {
	return &MockDatabase{products: make(map[string]model.Product)}
}

func (m *MockDatabase) CreateProduct(product model.Product) error {
	if _, exists := m.products[product.ID]; exists {
		return model.ErrDuplicateProductID
	}
	m.products[product.ID] = product
	return nil
}

func (m *MockDatabase) GetProduct(id string) (model.Product, error) {
	product, exists := m.products[id]
	if !exists {
		return model.Product{}, model.ErrProductNotFound
	}
	return product, nil
}

func (m *MockDatabase) SearchProducts(query string) ([]model.Product, error) {
	var results []model.Product
	for _, product := range m.products {
		if strings.Contains(strings.ToLower(product.Name), strings.ToLower(query)) {
			results = append(results, product)
		}
	}
	return results, nil
}

func (m *MockDatabase) UpdateProduct(product model.Product) error {
	if _, exists := m.products[product.ID]; !exists {
		return model.ErrProductNotFound
	}
	m.products[product.ID] = product
	return nil
}
