package logic

import (
	"errors"
	"time"
)

// Product is an example business entity,
// usually has a corresponding database table.
type Product struct {
	ID        string
	Name      string
	Price     int
	CreatedAt time.Time
}

var (
	ErrDuplicateProductID = errors.New("duplicate product ID")
	ErrProductNotFound    = errors.New("product not found")
)
