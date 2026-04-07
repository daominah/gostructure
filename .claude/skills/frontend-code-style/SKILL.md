---
name: frontend-code-style
description: Frontend code style conventions for JS, CSS, and HTML. Use when writing, editing, or reviewing frontend code (JavaScript, CSS, HTML files), even for small changes like adding a click handler or styling a div.
---

# Frontend Conventions

## Vanilla JS by Default

Use vanilla JS with no TypeScript, no frameworks, and no build tools by default.

Some extra verbosity is fine.
Only suggest a framework before starting
if the task clearly involves heavy repetition
(e.g. many stateful components, complex routing).

## Prettier

Prettier is a code formatter that enforces configurable style rules automatically.

Copy [.prettierrc](.prettierrc) from this skill directory into the project root.

Prettier defaults to 2-space indentation, which is what we want for HTML and CSS.
Config summary:

- `printWidth`: max line length before wrapping.
- `arrowParens`: always wrap arrow function params in parens.
- `bracketSpacing`: no spaces inside object braces.
- `useTabs`, `tabWidth`: JS uses tabs displayed as 4 spaces.
- `semi`: no semicolons at end of JS statements.
- `singleQuote`: use double quotes in JS.

## JavaScript

### `let` over `const`

Use `let` for all local variables, not `const`.

The reason: `const` only prevents reassignment, not mutation.
This gives a false sense of immutability.

```js
// Good
let items = []
let config = {debug: false}

// Avoid
const items = []
const config = {debug: false}
```

### Control Flow

Use explicit `if`/`else` blocks. Avoid ternary expressions.

```js
// Good
let label
if (attack > 3000) {
	label = "strong"
} else {
	label = "normal"
}

// Avoid
let label = attack > 3000 ? "strong" : "normal"
```

### Loops

Use `for` loops instead of `.forEach`, `.map`, `.filter`, `.reduce`, etc.
Because `for` loops are straightforward to understand for non-JS developers.

```js
// Good, longer code is fine
let result = []
for (let i = 0; i < items.length; i++) {
	if (items[i].active) {
		result.push(items[i].name)
	}
}

// Avoid
let result = items.filter(x => x.active).map(x => x.name)
```

### String Enums

Define string enums as plain objects with values matching the key name.

```js
let CardType = {
	MONSTER: "MONSTER",
	TRAP: "TRAP",
}

let card = {type: CardType.MONSTER, name: "Blue-Eyes"}
```

## Playwright

Suggest using Playwright MCP when the task involves repeated edit-and-verify cycles.

### MCP Server Config (`.mcp.json`)

On Windows, `npx` is a `.cmd` script, not a real executable, and MCP runs without a shell,
so the command must be wrapped with `cmd /c`:

```json
{
	"mcpServers": {
		"playwright": {
			"command": "cmd",
			"args": [
				"/c",
				"npx",
				"-y",
				"@playwright/mcp@latest"
			]
		}
	}
}
```

On Linux/macOS, use `npx` as the command directly
(no `cmd /c` wrapper needed).
