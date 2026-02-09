package httpsvr

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/daominah/gostructure/pkg/base"
	"github.com/daominah/gostructure/pkg/logic"
)

func TestAPICreateAndGetProduct(t *testing.T) {
	// GIVEN the API server handler (with mock database)
	apiHandler := NewHandlerAPI(logic.NewApp(logic.NewMockDatabase()))

	product0 := logic.Product{
		ID:    "test_product_API_" + base.NewUUID(),
		Name:  "Test Product API",
		Price: 300,
	}

	t.Run("POST /api/v1/product", func(t *testing.T) {
		reqBody, err := json.Marshal(product0)
		if err != nil {
			t.Fatalf("error json.Marshal: %v", err)
		}
		// WHEN call POST /api/v1/product
		req := httptest.NewRequest(http.MethodPost, "/api/v1/product", bytes.NewReader(reqBody))
		rsp := httptest.NewRecorder()
		apiHandler.ServeHTTP(rsp, req)
		// THEN successfully created product
		if rsp.Code != http.StatusCreated {
			t.Fatalf("CreateProductHandler returned status %d, want %d. got body: %s",
				rsp.Code, http.StatusCreated, rsp.Body.String())
		}
	})

	t.Run("POST /api/v1/product with duplicated product", func(t *testing.T) {
		reqBody, err := json.Marshal(product0)
		if err != nil {
			t.Fatalf("error json.Marshal: %v", err)
		}
		// WHEN call POST /api/v1/product with the same ID again
		req := httptest.NewRequest(http.MethodPost, "/api/v1/product", bytes.NewReader(reqBody))
		rsp := httptest.NewRecorder()
		apiHandler.ServeHTTP(rsp, req)
		// THEN status 409 duplicated error
		if rsp.Code != http.StatusConflict {
			t.Fatalf("error create product duplicate ID got status %d, want %d", rsp.Code, http.StatusConflict)
		}
	})

	t.Run("GET /api/v1/product/{id}", func(t *testing.T) {
		// WHEN call GET /api/v1/product/{id} with a valid id
		req := httptest.NewRequest(http.MethodGet, "/api/v1/product/"+product0.ID, nil)
		rsp := httptest.NewRecorder()
		apiHandler.ServeHTTP(rsp, req)
		// THEN successfully fetched product with expected data
		if rsp.Code != http.StatusOK {
			t.Fatalf("GetProductHandler returned status %d, want %d", rsp.Code, http.StatusOK)
		}
		var fetched logic.Product
		if err := json.NewDecoder(rsp.Body).Decode(&fetched); err != nil {
			t.Fatalf("failed to decode get response: %v", err)
		}
		if fetched.ID != product0.ID {
			t.Errorf("response got product ID: %q, want: %q", fetched.ID, product0.ID)
		}
		if fetched.Name != product0.Name {
			t.Errorf("response got product name: %q, want: %q", fetched.Name, product0.Name)
		}
		if fetched.Price != product0.Price {
			t.Errorf("response got product price: %d, want: %d", fetched.Price, product0.Price)
		}
	})

	t.Run("GET /api/v1/product/{id} with an invalid id", func(t *testing.T) {
		// WHEN call GET /api/v1/product/{id} with an invalid id
		req := httptest.NewRequest(http.MethodGet, "/api/v1/product/non_existing_id", nil)
		rsp := httptest.NewRecorder()
		apiHandler.ServeHTTP(rsp, req)
		// THEN get response status 404 Not Found
		if rsp.Code != http.StatusNotFound {
			t.Fatalf("GetProductHandler with invalid id returned status %d, want status %d. got body: %s",
				rsp.Code, http.StatusNotFound, rsp.Body.String())
		}
	})
}
