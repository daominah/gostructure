// Package logic contains business logic.
// The core logics can be tested without external resources
// (database, HTTP, websocket, message queue, file, ..),
// mock interfaces are used to simulate external resources in tests.
package logic

type App struct {
	Database Database
}

func NewApp(database Database) *App {
	return &App{Database: database}
}
