// Package core contains business logic. Can be tested without external
// resources (database, HTTP, websocket, message queue, file, ..)
package core

type App struct {
	database Database
}

func NewApp(database Database) *App {
	return &App{database: database}
}
