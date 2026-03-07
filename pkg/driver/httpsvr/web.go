package httpsvr

import (
	"net/http"

	"github.com/daominah/gostructure/web"
)

// NewHandlerWeb creates an HTTP handler that serves embedded static web files.
func NewHandlerWeb() http.Handler {
	handler := http.NewServeMux()
	handler.Handle("/", http.FileServerFS(web.FrontendAssets))
	return handler
}
