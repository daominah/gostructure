package httpsvr

import (
	"encoding/json"
	"errors"
	"fmt"
	"net/http"

	"github.com/daominah/gostructure/pkg/logic"
)

func CreateProductHandler(db logic.Database) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var product logic.Product
		if err := json.NewDecoder(r.Body).Decode(&product); err != nil {
			http.Error(w, fmt.Sprintf("invalid request body: %v", err), http.StatusBadRequest)
			return
		}

		err := db.CreateProduct(product)
		if err != nil {
			if errors.Is(err, logic.ErrDuplicateProductID) {
				http.Error(w, fmt.Sprintf("error CreateProduct: %v", err), http.StatusConflict)
				return
			}
			http.Error(w, fmt.Sprintf("error CreateProduct: %v", err), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
	}
}

func GetProductHandler(db logic.Database) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		id := r.PathValue("id")
		if id == "" {
			http.Error(w, "product id is required", http.StatusBadRequest)
			return
		}

		product, err := db.GetProduct(id)
		if err != nil {
			if errors.Is(err, logic.ErrProductNotFound) {
				http.Error(w, fmt.Sprintf("error GetProduct: %v", err), http.StatusNotFound)
				return
			}
			http.Error(w, fmt.Sprintf("error GetProduct: %v", err), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(product)
	}
}

func SearchProductsHandler(db logic.Database) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		query := r.URL.Query().Get("query")

		products, err := db.SearchProducts(query)
		if err != nil {
			http.Error(w, fmt.Sprintf("error SearchProducts: %v", err), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		_ = json.NewEncoder(w).Encode(products)
	}
}
