package database

import (
	"errors"
	"testing"

	"github.com/daominah/gostructure/pkg/base"
	"github.com/daominah/gostructure/pkg/logic"
)

func TestPostgresStore_Product(t *testing.T) {
	db := NewPostgresDatabase(globalTestConn)

	// GIVEN a product info
	product0ID := "test_product_" + base.NewUUID()
	product0 := logic.Product{ID: product0ID, Name: "Test Product 0", Price: 100}
	// WHEN creating the product THEN creation is successful
	err := db.CreateProduct(product0)
	if err != nil {
		t.Fatalf("error CreateProduct: %v", err)
	}

	// GIVEN the created product and its ID
	// WHEN retrieving the product by ID
	retrievedProduct, err := db.GetProduct(product0ID)
	if err != nil {
		t.Fatalf("error GetProduct: %v", err)
	}
	// THEN the retrieved product matches the created one
	product0.CreatedAt = retrievedProduct.CreatedAt // ignore field when comparison
	if retrievedProduct != product0 {
		t.Fatalf("retrieved product does not match created product: got %+v, want %+v", retrievedProduct, product0)
	}

	// WHEN try to read a non-existing product
	_, err = db.GetProduct("non_existing_id")
	// THEN an error is returned
	if err == nil {
		t.Fatalf("expected error when getting non_existing_id product, got nil")
	}

	// GIVEN another product
	product1ID := "test_product_" + base.NewUUID()
	product1 := logic.Product{ID: product1ID, Name: "Another Test Product", Price: 200}
	err = db.CreateProduct(product1)
	if err != nil {
		t.Fatalf("error CreateProduct for product1: %v", err)
	}
	// WHEN searching for products with "test_product" in their name
	products, err := db.SearchProducts("Test Product")
	if err != nil {
		t.Fatalf("error SearchProducts: %v", err)
	}
	// THEN both products are returned
	countMatched := 0
	for _, p := range products {
		if p.ID == product0.ID || p.ID == product1.ID {
			countMatched++
		}
	}
	if countMatched != 2 {
		t.Fatalf("expected both products to be in search results, got %d matched", countMatched)
	}

	// WHEN update a product
	updatedName := "Updated Test Product 0"
	updatedPrice := 150
	product0.Name, product0.Price = updatedName, updatedPrice
	err = db.UpdateProduct(product0)
	// THEN update is successful and read back reflects the changes
	if err != nil {
		t.Fatalf("error UpdateProduct: %v", err)
	}
	updatedProduct, err := db.GetProduct(product0ID)
	if err != nil {
		t.Fatalf("error GetProduct after update: %v", err)
	}
	if updatedProduct.Name != updatedName {
		t.Fatalf("error product info not updated, got name: %s, want: %s", updatedProduct.Name, updatedName)
	}
	if updatedProduct.Price != updatedPrice {
		t.Fatalf("error product info not updated, got price: %d, want: %d", updatedProduct.Price, updatedPrice)
	}

	// WHEN create a product with duplicate ID
	err = db.CreateProduct(product0)

	//t.Logf("debug err CreateProduct: %v", err)
	// Output: db.Exec INSERT duplicate product ID: ERROR: duplicate key value violates unique constraint "products_pkey" (SQLSTATE 23505)

	// THEN an expected error is returned
	if !errors.Is(err, logic.ErrDuplicateProductID) {
		t.Fatalf("got %v, want ErrDuplicateProductID", err)
	}
}
