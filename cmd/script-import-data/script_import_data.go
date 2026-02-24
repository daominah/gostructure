// this script is meant to be run as a one-off, not as a long-running service.
package main

import (
	"bytes"
	"encoding/csv"
	"fmt"
	"log"
	"strconv"
	"strings"

	"github.com/daominah/gostructure/pkg/base"
	"github.com/daominah/gostructure/pkg/model"
)

func main() {
	// example input data, probably read from a file in real usage
	csvData := []byte(`ID,Name,Price
IDUniqueA,ProductNameA,100
IDUniqueB,ProductNameProductB,200`)

	products, err := parseCSVProducts(csvData)
	if err != nil {
		log.Fatalf("failed to parse CSV: %v", err)
	}

	log.Printf("parsed %d products from CSV\n", len(products))
	for _, p := range products {
		log.Printf("product: %+v\n", p)
	}

	// connect to database ...

	// create products in database ...
}

func parseCSVProducts(csvData []byte) ([]model.Product, error) {
	csvReader := csv.NewReader(bytes.NewReader(csvData))
	rows, err := csvReader.ReadAll()
	if err != nil {
		return nil, fmt.Errorf("csvReader.ReadAll: %w", err)
	}
	if len(rows) < 2 {
		return nil, nil
	}

	// map Product struct fields to CSV column positions:
	colPos := make(map[string]int)
	for i, h := range rows[0] {
		colPos[strings.TrimSpace(h)] = i
	}
	colID, okID := colPos["ID"]
	colName, okName := colPos["Name"]
	colPrice, okPrice := colPos["Price"]
	if !okID || !okName || !okPrice {
		return nil, fmt.Errorf("CSV must have ID, Name and Price columns")
	}

	var products []model.Product
	for _, row := range rows[1:] {
		if len(row) <= colID || len(row) <= colName || len(row) <= colPrice {
			continue
		}
		id := strings.TrimSpace(row[colID])
		if id == "" {
			id = base.NewUUID()
		}
		name := strings.TrimSpace(row[colName])
		price, err := strconv.Atoi(strings.TrimSpace(row[colPrice]))
		if err != nil {
			return nil, fmt.Errorf("strconv.Atoi: %w", err)
		}
		products = append(products,
			model.Product{ID: id, Name: name, Price: price})
	}
	return products, nil
}
