package logic

type Database interface {
	CreateProduct(product Product) error
	GetProduct(id string) (Product, error)
	SearchProducts(query string) ([]Product, error)
	UpdateProduct(product Product) error
}
