// Package logic contains business logic.
// The core logics can be tested without external resources
// (database, HTTP, websocket, message queue, file, ..),
// mock interfaces are used to simulate external resources in tests.
package logic

import (
	"github.com/daominah/gostructure/pkg/base"
	"github.com/daominah/gostructure/pkg/model"
)

type App struct {
	Database Database
}

func NewApp(database Database) *App {
	return &App{Database: database}
}

func (a *App) CreateValidProduct(product model.Product) error {
	if product.ID == "" { // auto generate ID if not provided
		product.ID = base.NewUUID()
	}
	return a.Database.CreateProduct(product)
}

func (a *App) GetProduct(id string) (model.Product, error) {
	// here could be some additional business logic,
	// e.g. check user permissions, call other services, do some calculations, etc.
	// now this is just a simple pass-through to the database layer
	return a.Database.GetProduct(id)
}

func (a *App) SearchProducts(query string) ([]model.Product, error) {
	return a.Database.SearchProducts(query)
}
