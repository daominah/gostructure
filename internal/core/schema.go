package core

type Database interface {
	CreateUser(User) error
	ReadUser(username string) (User, error)
}

type User struct {
	Username       string
	HashedPassword string
	Email          string
}
