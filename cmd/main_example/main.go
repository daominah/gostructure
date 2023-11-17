package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/daominah/minah_struture/internal/core"
	"github.com/daominah/minah_struture/internal/driver/httpsvr"
)

func main() {
	log.SetFlags(log.Lshortfile)
	log.SetOutput(customLogger{})

	var database core.Database
	mysqlHost := os.Getenv("MYSQL_HOST")
	if mysqlHost != "" {
		log.Printf("recognized and used env var MYSQL_HOST=%v", mysqlHost)
	} else {
		log.Printf("empty env var MYSQL_HOST")
	}

	app := core.NewApp(database)
	go func() {
		listenPort := ":18282"
		log.Printf("serving API on http://localhost%v", listenPort)
		err := http.ListenAndServe(listenPort, httpsvr.NewHandlerAPI(app))
		if err != nil {
			log.Fatalf("error ListenAndServe: %v", err)
		}
	}()

	go func() {
		listenPort := ":18181"
		handler, err := httpsvr.NewHandlerGUI("")
		if err != nil {
			log.Fatalf("error NewHandlerGUI: %v", err)
		}
		log.Printf("serving user interface on http://localhost%v", listenPort)
		err = http.ListenAndServe(listenPort, handler)
		if err != nil {
			log.Fatalf("error ListenAndServe: %v", err)
		}
	}()

	select {}
}

// customLogger adds time to the beginning of each log line, write to stdout
type customLogger struct{}

func (writer customLogger) Write(bytes []byte) (int, error) {
	return fmt.Printf("%v %s", time.Now().UTC().Format("2006-01-02T15:04:05.000Z07:00"), bytes)
}
