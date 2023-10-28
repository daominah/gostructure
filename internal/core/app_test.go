package core

import (
	"testing"
)

func TestApp_User(t *testing.T) {
	app := NewApp(NewMockDatabase())
	err := app.UserRegister(UserRegisterRequest{
		Username: "haha",
		Password: "123456",
		Email:    "hohohaha@gmail.com",
	})
	if err != nil {
		t.Fatalf("error app.UserRegister: %v", err)
	}
	_, err = app.UserLogin(UserLoginRequest{Username: "haha1", Password: "123456"})
	if err != ErrUserNotFound {
		t.Errorf("error UserLoginRequest got %v but want %v", err, ErrUserNotFound)
	}
	_, err = app.UserLogin(UserLoginRequest{Username: "haha", Password: "123"})
	if err != ErrUserLoginWrongPassword {
		t.Errorf("error UserLoginRequest got %v but want %v", err, ErrUserLoginWrongPassword)
	}
	_, err = app.UserLogin(UserLoginRequest{Username: "haha", Password: "123456"})
	if err != nil {
		t.Errorf("error UserLoginRequest got %v but want %v", err, nil)
	}
}
