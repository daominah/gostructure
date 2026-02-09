package main

import (
	"database/sql"
	"log"
	"net/http"
	"os"

	"github.com/daominah/gostructure/pkg/driver/database"
	"github.com/daominah/gostructure/pkg/driver/httpsvr"
	"github.com/daominah/gostructure/pkg/logic"
	_ "github.com/jackc/pgx/v5/stdlib"
	"github.com/joho/godotenv"
)

func main() {
	// Load environment variables from config/.env or config/.env.example,
	// func Load will not override existing envs, so priority is:
	// envs from host/container > file .env > file .env.example.
	if err := godotenv.Load("config/.env"); err != nil {
		if err := godotenv.Load("config/.env.example"); err != nil {
			log.Printf("no .env files found, using environment variables")
		}
	}

	// Connect to external dependencies:

	// Connect to database PostgreSQL
	dbHost := os.Getenv("POSTGRES_HOST")
	dbPort := os.Getenv("POSTGRES_PORT")
	dbName := os.Getenv("POSTGRES_DB")
	dbUser := os.Getenv("POSTGRES_USER")
	dbPassword := os.Getenv("POSTGRES_PASSWORD")
	if dbHost == "" || dbPort == "" || dbName == "" || dbUser == "" || dbPassword == "" {
		log.Fatal("POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD environment variables are required")
	}
	dbURL, err := database.BuildConnectionString(dbHost, dbPort, dbName, dbUser, dbPassword)
	if err != nil {
		log.Fatal(err)
	}
	dbPool, err := sql.Open("pgx", dbURL)
	if err != nil {
		log.Fatalf("failed to open database: %v", err)
	}
	if err := dbPool.Ping(); err != nil {
		log.Fatalf("failed to ping database: %v", err)
	}
	defer dbPool.Close()

	// conveniently run database migrations on startup, careful with production usage
	if err := database.RunDatabaseMigrations(dbPool); err != nil {
		log.Fatalf("failed to run database migrations: %v", err)
	}

	// Initialize application object that holds all dependencies for handlers
	var postgresDB logic.Database
	postgresDB = database.NewPostgresDatabase(dbPool)

	app := logic.NewApp(postgresDB)

	// Set up HTTP server

	webHandler, err := httpsvr.NewHandlerWeb("")
	if err != nil {
		log.Fatalf("failed to create web handler: %v", err)
	}
	mux := http.NewServeMux()
	mux.Handle("/api/v1/", httpsvr.NewHandlerAPI(app))
	mux.Handle("/", webHandler)

	port := os.Getenv("LISTENING_PORT")
	if port == "" {
		port = "20808"
	}
	log.Printf("server is listening on http://localhost:%s/", port)
	err = http.ListenAndServe(":"+port, mux)
	if err != nil {
		log.Fatalf("error FATAL cannot start the server: http.ListenAndServe: %v", err)
	}
}
