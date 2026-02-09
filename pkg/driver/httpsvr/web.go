package httpsvr

import (
	"fmt"
	"log"
	"net/http"
	"path/filepath"

	"github.com/daominah/gostructure/pkg/base"
)

// NewHandlerWeb creates an HTTP handler that serves static files from the web directory.
// The handler serves files from the specified webDirPath, or defaults to the project's web directory.
// Note: Consider using embed.FS to embed web files in the binary to avoid filesystem dependency.
func NewHandlerWeb(webDirPath string) (http.Handler, error) {
	if webDirPath == "" {
		projectRoot, err := base.GetProjectRootDir()
		if err != nil {
			return nil, fmt.Errorf("empty webDirPath and cannot GetProjectRootDir: %w", err)
		}
		webDirPath = filepath.Join(projectRoot, "web")
		log.Printf("empty path for web app static directory, use the default location: %v", webDirPath)
	}
	handler := http.NewServeMux()
	handler.Handle("/", http.FileServer(http.Dir(webDirPath)))
	return handler, nil
}
