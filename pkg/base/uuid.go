package base

import (
	"github.com/google/uuid"
)

// NewUUID generates UUIDv7 strings that are lexicographically sortable by creation time.
//
// UUIDv7 starts with a 48-bit Unix timestamp (milliseconds since epoch),
// followed by version/variant bits and random bits (the remaining 80 bits).
// The timestamp is stored in the first 12 hex characters of the UUID string.
//
// Because the timestamp is at the beginning, records can be sorted
// chronologically using simple string comparison (ORDER BY id ASC) without
// relying on a separate created_at column.
//
// Example: Two UUIDs generated at different times will sort correctly:
//   - Earlier UUID: "018f1234-5678-7abc-def0-123456789abc"
//   - Later UUID:   "018f5678-9abc-7def-0123-456789abcdef"
//     When sorted alphabetically, earlier UUIDs come first.
func NewUUID() string {
	return uuid.Must(uuid.NewV7()).String()
}
