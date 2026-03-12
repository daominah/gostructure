// Combine .claude/skills/*/SKILL.md into .github/copilot_personalization.md.
// Only includes skill directories that contain exactly one file (SKILL.md).
// Run from project root: go run .github/copilot_from_skills.go
package main

import (
	"log"
	"os"
	"path/filepath"
	"sort"
	"strings"
)

func main() {
	skillsDir := ".claude/skills"
	outputPath := ".github/copilot_personalization.md"

	// excludedSkills lists skill directory names to skip when generating the output.
	var excludedSkills = map[string]bool{
		"reviewing-code-and-pr": true, // long 4711 chars, not really helpful on remote AI
	}

	entries, err := os.ReadDir(skillsDir)
	if err != nil {
		log.Fatalf("error os.ReadDir %s: %v", skillsDir, err)
	}

	// Collect skill dirs that contain only SKILL.md
	var skillNames []string
	for _, e := range entries {
		if !e.IsDir() {
			continue
		}
		dirPath := filepath.Join(skillsDir, e.Name())
		files, err := os.ReadDir(dirPath)
		if err != nil {
			log.Fatalf("error os.ReadDir %s: %v", dirPath, err)
		}
		if len(files) == 1 && files[0].Name() == "SKILL.md" && !excludedSkills[e.Name()] {
			skillNames = append(skillNames, e.Name())
		}
	}
	sort.Strings(skillNames)

	// Read each SKILL.md, strip frontmatter, collect body
	var parts []string
	var skillLengths = make(map[string]int)
	var totalLength int
	for _, name := range skillNames {
		path := filepath.Join(skillsDir, name, "SKILL.md")
		content, err := os.ReadFile(path)
		if err != nil {
			log.Fatalf("error os.ReadFile %s: %v", path, err)
		}
		body := stripFrontmatter(string(content))
		if body != "" {
			skillLengths[name] = len(body)
			totalLength += len(body)
			parts = append(parts, body)
		}
	}

	// Skills consume Language Model context, print lengths here, so we are aware
	for _, name := range skillNames {
		if length, ok := skillLengths[name]; ok {
			pct := 0.0
			if totalLength > 0 {
				pct = 100 * float64(length) / float64(totalLength)
			}
			log.Printf("len: %4d, percent: %2.0f%%, skill: %s", length, pct, name)
		}
	}

	output := strings.Join(parts, "\n\n")
	if err := os.WriteFile(outputPath, []byte(output), 0644); err != nil {
		log.Fatalf("error os.WriteFile %s: %v", outputPath, err)
	}
	const copilotLimit = 8000
	log.Printf("========================================")
	log.Printf("Wrote %v characters to %s", len(output), outputPath)
	estimatedTokens := len(output) / 4
	log.Printf("equivalent to %d tokens (assuming 1 token ≈ 4 characters)", estimatedTokens)
	if len(output) > copilotLimit {
		log.Printf("WARNING: exceeds Copilot limit of %d characters by %d", copilotLimit, len(output)-copilotLimit)
	}
}

// stripFrontmatter removes the YAML frontmatter block (--- ... ---) from the beginning of content.
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
