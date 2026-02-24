package base

import (
	"golang.org/x/crypto/bcrypt"
)

// HashPassword returns the hash of input plain password for secure storage.
// Note that in this brcypt implementation, there is a 72-chars limit for password length,
// change to a more complex algorithm if needed and make sure to update VerifyPassword accordingly.
func HashPassword(password string) (string, error) {
	hash, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return "", err
	}
	return string(hash), nil
}

// VerifyPassword returns true if the plain password matches the hash.
// Must use the same algorithm as func HashPassword.
func VerifyPassword(hashed, password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(hashed), []byte(password))
	return err == nil
}
