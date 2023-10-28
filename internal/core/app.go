// Package core contains business logic. Can be tested without external
// resources (database, HTTP, websocket, message queue, file, ..)
package core

import (
	"fmt"
	"log"

	"golang.org/x/crypto/bcrypt"
)

type App struct {
	database Database
}

func NewApp(database Database) *App { return &App{database: database} }

func (a *App) UserRegister(r UserRegisterRequest) error {
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(r.Password), bcrypt.DefaultCost)
	if err != nil {
		return fmt.Errorf("bcrypt.GenerateFromPassword %v", err)
	}
	err = a.database.CreateUser(User{
		Username:       r.Username,
		HashedPassword: string(hashedPassword),
		Email:          r.Email,
	})
	if err != nil {
		return fmt.Errorf("database.CreateUser: %v", err)
	}
	return nil
}

type UserRegisterRequest struct {
	Username string
	Password string
	Email    string
}

func (a *App) UserLogin(r UserLoginRequest) (UserLoginResponse, error) {
	user, err := a.database.ReadUser(r.Username)
	if err != nil {
		if err != ErrUserNotFound {
			log.Printf("error internal server database.ReadUser: %v\n", err)
			return UserLoginResponse{}, err
		}
		return UserLoginResponse{}, ErrUserNotFound
	}
	err = bcrypt.CompareHashAndPassword([]byte(user.HashedPassword), []byte(r.Password))
	if err != nil {
		return UserLoginResponse{}, ErrUserLoginWrongPassword
	}
	return UserLoginResponse{SetCookie: "ExampleJWTTokenContainUserData"}, nil
}

type UserLoginRequest struct {
	Username string
	Password string
}

type UserLoginResponse struct {
	SetCookie string
}

var ErrUserNotFound = fmt.Errorf("user not found")
var ErrUserLoginWrongPassword = fmt.Errorf("wrong password")
