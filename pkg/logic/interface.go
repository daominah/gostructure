package logic

import "github.com/daominah/gostructure/pkg/model"

type Database interface {
	CreateProduct(product model.Product) error
	GetProduct(id string) (model.Product, error)
	SearchProducts(query string) ([]model.Product, error)
	UpdateProduct(product model.Product) error
}
