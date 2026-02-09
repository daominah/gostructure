package database

import (
	"database/sql"
	"embed"
	"fmt"
	"log"

	goose "github.com/pressly/goose/v3"
)

//go:embed migration/*.sql
var migrationFiles embed.FS

// BuildConnectionString creates a PostgreSQL connection string from the provided parameters
// and logs it with masked password for security.
// Returns the connection string and an error if any required parameter is empty.
func BuildConnectionString(host, port, dbName, user, password string) (string, error) {
	if host == "" || port == "" || dbName == "" || user == "" || password == "" {
		return "", fmt.Errorf("host, port, dbName, user, and password parameters are required")
	}
	connStrFormat := "postgres://%s:%s@%s:%s/%s?sslmode=disable"
	connStr := fmt.Sprintf(connStrFormat, user, password, host, port, dbName)
	maskedConnStr := fmt.Sprintf(connStrFormat, user, "****", host, port, dbName)
	log.Printf("database connection: %s", maskedConnStr)
	return connStr, nil
}

// RunDatabaseMigrations applies all pending database schema changes.
// Suitable for development, but consider this on production carefully.
func RunDatabaseMigrations(db *sql.DB) error {
	if err := goose.SetDialect("postgres"); err != nil {
		return err
	}
	goose.SetBaseFS(migrationFiles)
	if err := goose.Up(db, "migration"); err != nil {
		return err
	}
	return nil
}

// PostgresDatabase implements logic.Database interface using PostgreSQL
type PostgresDatabase struct {
	db *sql.DB
}

// NewPostgresDatabase creates a new PostgresDatabase instance
func NewPostgresDatabase(db *sql.DB) *PostgresDatabase {
	return &PostgresDatabase{db: db}
}

// usual expected Postgres error codes, used for error matching
const (
	// ErrorCodeUniqueViolation happens when creating a row with duplicate primary key or unique key
	ErrorCodeUniqueViolation = "23505"
)
