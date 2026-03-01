// Combine .cursor/rules/*.mdc into .github/copilot-instructions.md.
// Run from project root: go run .github/copilot_from_cursor_rules.go
package main

import (
	"log"
	"os"
	"path/filepath"
	"sort"
	"strings"
)

func main() {
	rulesDir := ".cursor/rules"
	outputPath := ".github/copilot-instructions.md"

	// Read all Cursor rules from .cursor/rules
	entries, err := os.ReadDir(rulesDir)
	if err != nil {
		log.Fatalf("error os.ReadDir %s: %v", rulesDir, err)
	}

	// Collect all .mdc rule filenames and sort by name
	var names []string
	for _, e := range entries {
		if !e.IsDir() && strings.HasSuffix(e.Name(), ".mdc") {
			names = append(names, e.Name())
		}
	}
	sort.Strings(names)

	// Read each rule, strip frontmatter (--- ... alwaysApply ... ---), collect body
	var parts []string
	var ruleLengths = make(map[string]int)
	var totalLength int
	for _, name := range names {
		path := filepath.Join(rulesDir, name)
		content, err := os.ReadFile(path)
		if err != nil {
			log.Fatalf("error os.ReadFile %s: %v", path, err)
		}
		body := stripFrontmatter(string(content))
		if body != "" {
			ruleLengths[name] = len(body)
			totalLength += len(body)
			parts = append(parts, body)
		}
	}

	// Rules consume Language Model context, print lengths here, so we are aware
	for _, name := range names {
		if length, ok := ruleLengths[name]; ok {
			pct := 0.0
			if totalLength > 0 {
				pct = 100 * float64(length) / float64(totalLength)
			}
			log.Printf("len: %4d, percent: %2.0f%%, rule: %s", length, pct, name)
		}
	}

	// Combine all rule bodies and write to copilot-instructions.md
	output := strings.Join(parts, "\n\n")
	if err := os.WriteFile(outputPath, []byte(output), 0644); err != nil {
		log.Fatalf("error os.WriteFile %s: %v", outputPath, err)
	}
	log.Printf("Wrote %v characters to %s", len(output), outputPath)
}

// stripFrontmatter removes the YAML frontmatter block (--- ... alwaysApply ... ---)
// at the beginning of the rule content
func stripFrontmatter(content string) string {
	const delim = "---"
	first := strings.Index(content, delim)
	if first == -1 {
		return strings.TrimSpace(content)
	}
	rest := content[first+len(delim):]
	second := strings.Index(rest, delim)
	if second == -1 {
		return strings.TrimSpace(content)
	}
	return strings.TrimSpace(rest[second+len(delim):])
}
