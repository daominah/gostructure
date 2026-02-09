package database

import (
	"database/sql"
	"log"
	"os"
	"testing"

	_ "github.com/daominah/gostructure/pkg/base"
	"github.com/daominah/gostructure/pkg/logic"
	_ "github.com/jackc/pgx/v5/stdlib"
)

// globalTestConn is a shared database connection used by all tests in the database package.
// It is initialized in TestMain and should not be modified by individual tests.
var globalTestConn *sql.DB

func TestMain(m *testing.M) {
	// based on docker-compose.yml, connect to local database
	host, port, dbName, user, password := "localhost", "25432", "gostructure", "user", "password"
	connStr, err := BuildConnectionString(host, port, dbName, user, password)
	if err != nil {
		log.Fatalf("BuildConnectionString failed: %v", err)
	}
	globalTestConn, err = sql.Open("pgx", connStr)
	if err != nil {
		log.Fatalf("failed to open db: %v", err)
	}
	if err := globalTestConn.Ping(); err != nil {
		log.Fatalf("failed to ping db: %v", err)
	}
	if err := RunDatabaseMigrations(globalTestConn); err != nil {
		log.Fatalf("RunDatabaseMigrations failed: %v", err)
	}
	code := m.Run()
	_ = globalTestConn.Close()
	os.Exit(code)
}

func TestPostgresDatabaseImplementsDatabaseInterface(t *testing.T) {
	var _ logic.Database = &PostgresDatabase{}
}
