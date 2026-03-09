package httpsvr

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"

	"github.com/daominah/gostructure/pkg/logic"
	"github.com/daominah/gostructure/pkg/model"
)

func CreateProductHandler(app *logic.App) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var product model.Product
		if err := json.NewDecoder(r.Body).Decode(&product); err != nil {
			http.Error(w, fmt.Sprintf("invalid request body: %v", err), http.StatusBadRequest)
			return
		}

		err := app.CreateValidProduct(product)
		if err != nil {
			if errors.Is(err, model.ErrDuplicateProductID) {
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

func GetProductHandler(app *logic.App) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		id := r.PathValue("id")
		if id == "" {
			http.Error(w, "product id is required", http.StatusBadRequest)
			return
		}

		product, err := app.GetProduct(id)
		if err != nil {
			if errors.Is(err, model.ErrProductNotFound) {
				http.Error(w, fmt.Sprintf("error GetProduct: %v", err), http.StatusNotFound)
				return
			}
			http.Error(w, fmt.Sprintf("error GetProduct: %v", err), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(product); err != nil {
			log.Printf("error encoding response: %v", err)
		}
	}
}

func SearchProductsHandler(app *logic.App) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		query := r.URL.Query().Get("query")

		products, err := app.SearchProducts(query)
		if err != nil {
			http.Error(w, fmt.Sprintf("error SearchProducts: %v", err), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		if err := json.NewEncoder(w).Encode(products); err != nil {
			log.Printf("error encoding response: %v", err)
		}
	}
}
