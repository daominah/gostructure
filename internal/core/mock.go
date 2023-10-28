package core

import (
	"sync"
)

type MockDatabase struct {
	users map[string]User
	mutex *sync.Mutex
}

func NewMockDatabase() *MockDatabase {
	return &MockDatabase{users: make(map[string]User), mutex: &sync.Mutex{}}
}

func (db *MockDatabase) CreateUser(user User) error {
	db.mutex.Lock()
	defer db.mutex.Unlock()
	db.users[user.Username] = user
	return nil
}

func (db *MockDatabase) ReadUser(username string) (User, error) {
	db.mutex.Lock()
	defer db.mutex.Unlock()
	user, found := db.users[username]
	if !found {
		return User{}, ErrUserNotFound
	}
	return user, nil
}
