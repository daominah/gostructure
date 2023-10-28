// Package httpsvr is an HTTP server that allows users to interact with the app
package httpsvr

import (
	"net/http"

	"github.com/daominah/minah_struture/internal/core"
)

// TODO: better httpsvr.NewHandlerAPI example:
// create struct Handle that has a field is App so we can add method to the Handle,
// the Handle can call App methods, then we can convert App result and error to
// corresponding HTTP status, header, body

func NewHandlerAPI(app *core.App) http.Handler {
	handler := http.NewServeMux()
	handler.HandleFunc("/", func() http.HandlerFunc {
		return func(w http.ResponseWriter, r *http.Request) {
			w.Write([]byte("http handler that calls struct App methods"))
		}
	}())
	return handler
}
