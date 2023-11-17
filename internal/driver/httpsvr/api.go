// Package httpsvr is an HTTP server that allows users to interact with the app
package httpsvr

import (
	"net/http"

	"github.com/daominah/minah_struture/internal/core"
)

func NewHandlerAPI(app *core.App) http.Handler {
	handler := http.NewServeMux()
	handler.HandleFunc("/", func() http.HandlerFunc {
		return func(w http.ResponseWriter, r *http.Request) {
			w.Write([]byte("http handler that calls struct App methods"))
		}
	}())
	return handler
}
