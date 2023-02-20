package main

import (
	"fmt"
	"log"
	"os"
	"time"
)

func main() {
	log.SetFlags(log.Lshortfile)
	log.SetOutput(customLogger{})

	mysqlHost := os.Getenv("MYSQL_HOST")
	if mysqlHost != "" {
		log.Printf("recognized and used env var MYSQL_HOST=%v", mysqlHost)
	} else {
		log.Printf("empty env var MYSQL_HOST")
	}

	for i := 0; true; i++ {
		log.Printf("executable example is running: %v", i)
		time.Sleep(1 * time.Second)
	}
}

type customLogger struct{}

func (writer customLogger) Write(bytes []byte) (int, error) {
	return fmt.Printf("%v\t%s", time.Now().UTC().Format("2006-01-02T15:04:05.000Z07:00"), bytes)
}
