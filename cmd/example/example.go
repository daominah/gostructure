package main

import (
	"os"
	"time"

	"github.com/mywrap/log"
)

func main() {
	mysqlHost := os.Getenv("MYSQL_HOST")
	log.Printf("recognized and used env var MYSQL_HOST=%v", mysqlHost)

	for i := 0; true; i++ {
		log.Printf("executable example is running: %v", i)
		time.Sleep(1 * time.Second)
	}
}
