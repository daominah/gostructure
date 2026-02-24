package base

import (
	"log"
	"sort"
	"strings"
	"testing"
	"time"
)

func TestCustomLogger(t *testing.T) {
	log.Printf("TestCustomLogger log.Printf")
	// Output: YYYY-mm-ddTHH:MM:SS.999+07:00 base_test.go:9: TestCustomLogger log.Printf

	t.Logf("TestCustomLogger t.Logf")
	// Output without timestamp
}

func TestGetProjectRootDir(t *testing.T) {
	projectRootDir, err := GetProjectRootDir()
	if err != nil {
		t.Fatalf("error GetProjectRootDir: %v", err)
	}
	t.Logf("projectRootDir: %s", projectRootDir)
	// Output: HOME/go/src/github.com/daominah/gostructure
	if !strings.HasSuffix(projectRootDir, "gostructure") {
		t.Errorf("error GetProjectRootDir: got %s, want gostructure suffix", projectRootDir)
	}
}

func TestNewUUID(t *testing.T) {
	// GIVEN: Generate multiple UUIDs with 10ms sleep between each
	const numUUIDs = 5
	uuids := make([]string, numUUIDs)
	for i := 0; i < numUUIDs; i++ {
		uuids[i] = NewUUID()
		time.Sleep(10 * time.Millisecond)
	}

	// WHEN: Sort the UUIDs lexicographically
	sortedUUIDs := make([]string, len(uuids))
	copy(sortedUUIDs, uuids)
	sort.Strings(sortedUUIDs)

	// THEN: Verify the order stays the same after sorting
	for i := 0; i < len(uuids); i++ {
		if uuids[i] != sortedUUIDs[i] {
			t.Errorf("UUID order changed after sorting: expected %s at index %d, got %s", uuids[i], i, sortedUUIDs[i])
		}
	}
}

func TestHashPassword(t *testing.T) {
	// GIVEN a plain password
	password := "test-secret-123"

	// WHEN hashing the password
	hash, err := HashPassword(password)
	if err != nil {
		t.Fatalf("HashPassword: %v", err)
	}
	if hash == "" {
		t.Fatal("hash should not be empty")
	}

	// THEN VerifyPassword accepts the correct password
	if !VerifyPassword(hash, password) {
		t.Error("VerifyPassword should return true for correct password")
	}

	// AND rejects wrong password
	if VerifyPassword(hash, "wrong") {
		t.Error("VerifyPassword should return false for wrong password")
	}
}
