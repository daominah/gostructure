package database

import (
	"database/sql"
	"errors"
	"fmt"
	"time"

	"github.com/daominah/gostructure/pkg/logic"
	"github.com/jackc/pgx/v5/pgconn"
)

// CreateProduct creates a new product in the database
func (p *PostgresDatabase) CreateProduct(product logic.Product) error {
	createdAt := product.CreatedAt
	if createdAt.IsZero() {
		createdAt = time.Now()
	}
	query := `INSERT INTO products (id, name, price, created_at) VALUES ($1, $2, $3, $4)`
	_, err := p.db.Exec(query, product.ID, product.Name, product.Price, createdAt)
	if err != nil {
		var pgErr *pgconn.PgError
		if errors.As(err, &pgErr) && pgErr.Code == ErrorCodeUniqueViolation {
			return fmt.Errorf("%w: %v, db.Exec INSERT: %w",
				logic.ErrDuplicateProductID, product.ID, err)
		}
		return fmt.Errorf("db.Exec INSERT: %w", err)
	}
	return nil
}

// GetProduct retrieves a product by ID
func (p *PostgresDatabase) GetProduct(id string) (logic.Product, error) {
	var product logic.Product
	query := `SELECT id, name, price, created_at FROM products WHERE id = $1`
	err := p.db.QueryRow(query, id).Scan(&product.ID, &product.Name, &product.Price, &product.CreatedAt)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return logic.Product{}, fmt.Errorf("%w: %v, db.QueryRow SELECT: %w",
				logic.ErrProductNotFound, id, err)
		}
		return logic.Product{}, fmt.Errorf("db.QueryRow SELECT: %w", err)
	}
	return product, nil
}

// SearchProducts searches for products by name
func (p *PostgresDatabase) SearchProducts(query string) ([]logic.Product, error) {
	sqlQuery := `SELECT id, name, price, created_at FROM products WHERE name ILIKE $1 ORDER BY id DESC`
	rows, err := p.db.Query(sqlQuery, "%"+query+"%")
	if err != nil {
		return nil, fmt.Errorf("db.Query SELECT ILIKE: %w", err)
	}
	defer rows.Close()

	var products []logic.Product
	for rows.Next() {
		var product logic.Product
		if err := rows.Scan(&product.ID, &product.Name, &product.Price, &product.CreatedAt); err != nil {
			return nil, fmt.Errorf("rows.Scan: %w", err)
		}
		products = append(products, product)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("rows.Err: %w", err)
	}
	return products, nil
}

// UpdateProduct updates an existing product
func (p *PostgresDatabase) UpdateProduct(product logic.Product) error {
	query := `UPDATE products SET name = $2, price = $3 WHERE id = $1`
	result, err := p.db.Exec(query, product.ID, product.Name, product.Price)
	if err != nil {
		return fmt.Errorf("db.Exec UPDATE: %w", err)
	}
	rowsAffected, err := result.RowsAffected()
	if err != nil {
		return fmt.Errorf("result.RowsAffected: %w", err)
	}
	if rowsAffected == 0 {
		return fmt.Errorf("%w: %v, db.Exec UPDATE 0 rowsAffected", logic.ErrProductNotFound, product.ID)
	}
	return nil
}
