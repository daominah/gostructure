// Combine .cursor/rules/*.mdc into .github/copilot-instructions.md.
// Run from project root: go run .github/copilot_from_cursor_rules.go
package main

import (
	"fmt"
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
		fmt.Fprintf(os.Stderr, "error os.ReadDir %s: %v\n", rulesDir, err)
		os.Exit(1)
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
	for _, name := range names {
		path := filepath.Join(rulesDir, name)
		content, err := os.ReadFile(path)
		if err != nil {
			fmt.Fprintf(os.Stderr, "error os.ReadFile %s: %v\n", path, err)
			os.Exit(1)
		}
		body := stripFrontmatter(string(content))
		if body != "" {
			parts = append(parts, body)
		}
	}

	// Combine all rule bodies and write to copilot-instructions.md
	output := strings.Join(parts, "\n\n")
	if err := os.WriteFile(outputPath, []byte(output), 0644); err != nil {
		fmt.Fprintf(os.Stderr, "error os.WriteFile %s: %v\n", outputPath, err)
		os.Exit(1)
	}
	fmt.Printf("Wrote %s\n", outputPath)
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
