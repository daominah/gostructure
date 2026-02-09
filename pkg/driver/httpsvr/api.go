package httpsvr

import (
	"net/http"

	"github.com/daominah/gostructure/pkg/logic"
)

// NewHandlerAPI creates an HTTP handler for API endpoints.
func NewHandlerAPI(app *logic.App) http.Handler {
	mux := http.NewServeMux()

	// Product endpoints
	mux.HandleFunc("POST /api/v1/product", CreateProductHandler(app.Database))
	mux.HandleFunc("GET /api/v1/product/{id}", GetProductHandler(app.Database))
	mux.HandleFunc("GET /api/v1/product", SearchProductsHandler(app.Database))

	return mux
}
