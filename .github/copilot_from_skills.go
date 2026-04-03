// Combine .claude/skills/*/SKILL.md and sections from .claude/CLAUDE.md
// into .github/copilot_personalization.md.
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
		"adding-feature-ticket": true, // full flow with tools for local agent
		"fixing-bug-ticket":     true, // full flow with tools for local agent
		"go-project-structure":  true, // Copilot usually only focuses on one file
		"reviewing-code-and-pr": true, // long, not really helpful on remote AI
		"slack-messaging":       true, // Copilot cannot send Slack anyway
		"sql-formatting":        true, // result can be easily formatted by IDE
	}

	// stripSections maps skill names to section headers to remove from their content.
	var stripSections = map[string][]string{
		"writing-style-markdown": {"### Example"},
	}

	// claudeMD sections to extract by header (included before skills).
	claudeMD := ".claude/CLAUDE.md"
	claudeSections := []string{
		"# Writing Style",
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
		for _, header := range stripSections[name] {
			body = removeSection(body, header)
		}
		if body != "" {
			skillLengths[name] = len(body)
			totalLength += len(body)
			parts = append(parts, body)
		}
	}

	// Extract configured sections from CLAUDE.md
	claudeContent, err := os.ReadFile(claudeMD)
	if err != nil {
		log.Fatalf("error os.ReadFile %s: %v", claudeMD, err)
	}
	for _, header := range claudeSections {
		section := extractSection(string(claudeContent), header)
		if section == "" {
			continue
		}
		name := "CLAUDE.md:" + strings.TrimLeft(header, "# ")
		skillLengths[name] = len(section)
		totalLength += len(section)
		skillNames = append(skillNames, name)
		parts = append(parts, section)
	}

	// print length of each instruction
	for _, name := range skillNames {
		if length, ok := skillLengths[name]; ok {
			pct := 0.0
			if totalLength > 0 {
				pct = 100 * float64(length) / float64(totalLength)
			}
			log.Printf("len: %4d, percent: %2.0f%%, skill: %s", length, pct, name)
		}
	}

	output := strings.Join(parts, "\n\n") + "\n"
	if err := os.WriteFile(outputPath, []byte(output), 0644); err != nil {
		log.Fatalf("error os.WriteFile %s: %v", outputPath, err)
	}
	const copilotLimit = 4000
	log.Printf("========================================")
	log.Printf("Wrote %v characters to %s", len(output), outputPath)
	estimatedTokens := len(output) / 4
	log.Printf("equivalent to %d tokens (assuming 1 token ≈ 4 characters)", estimatedTokens)
	if len(output) > copilotLimit {
		log.Printf("WARNING: exceeds Copilot soft limit of %d characters by %d", copilotLimit, len(output)-copilotLimit)
	}
}

// extractSection extracts a markdown section by its exact header line.
// It returns the header and all content until the next header of equal or higher level.
func extractSection(content, header string) string {
	idx := strings.Index(content, header+"\n")
	if idx == -1 {
		return ""
	}
	rest := content[idx+len(header)+1:]
	// Determine the header level (count leading '#' characters)
	level := 0
	for _, ch := range header {
		if ch == '#' {
			level++
		} else {
			break
		}
	}
	// Find the next header of equal or higher level
	lines := strings.Split(rest, "\n")
	var end int
	found := false
	for i, line := range lines {
		if strings.HasPrefix(line, strings.Repeat("#", level)+" ") || line == strings.Repeat("#", level) {
			end = i
			found = true
			break
		}
	}
	if found {
		rest = strings.Join(lines[:end], "\n")
	}
	return strings.TrimSpace(header + "\n" + rest)
}

// removeSection removes a markdown section (header and body) from content.
// It finds the section by exact header match and removes everything until
// the next header of equal or higher level.
func removeSection(content, header string) string {
	section := extractSection(content, header)
	if section == "" {
		return content
	}
	return strings.TrimSpace(strings.Replace(content, section, "", 1))
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
