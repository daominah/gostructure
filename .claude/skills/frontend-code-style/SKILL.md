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
- `bracketSpacing: false`: no spaces inside object braces.
- `useTabs`, `tabWidth`: JS uses tabs displayed as 4 spaces.
- `semi: false`: no semicolons at end of JS statements.
- `singleQuote: false`: use double quotes in JS.

## JavaScript

Prefer explicit, standard syntax over shorthand or syntactic sugar.
Longer code is acceptable; the goal is clarity that does not require
JavaScript-specific knowledge to read.

### Conditional Branching

Use explicit `if`/`else` blocks. Avoid ternary expressions.

Good:

```js
let label
if (attack > 3000) {
	label = "strong"
} else {
	label = "normal"
}
```

Avoid:

```js
let label = attack > 3000 ? "strong" : "normal"
```

### Loops

Use `for` loops instead of `.forEach`, `.map`, `.filter`, `.reduce`, etc.
Because `for` loops are straightforward to understand for non-JS developers.

Good:

```js
let result = []
for (let i = 0; i < items.length; i++) {
	if (items[i].active) {
		result.push(items[i].name)
	}
}
```

Avoid:

```js
let result = items.filter(x => x.active).map(x => x.name)
```

### Declare Variables with `let`

Use `let` for all local variables, not `const`.

The reason: `const` only prevents reassignment, not mutation.
This gives a false sense of immutability.

Good:

```js
let items = []
let config = {debug: false}
```

Avoid:

```js
const items = []
const config = {debug: false}
```

### String Enums

Whenever a field or variable holds one of a fixed set of predefined values,
define a string enum object instead of using raw strings inline.
Use PascalCase for both keys and values, matching the key name exactly.
Avoid numeric codes.

Good:

```js
let CardType = {
	Monster: "Monster",
	Spell: "Spell",
	Trap: "Trap",
}

let card = {type: CardType.Monster, name: "Blue-Eyes"}
```

Avoid (raw string inline):

```js
let card = {type: "Monster", name: "Blue-Eyes"}
```

### Function Definitions

Use function declarations as the default.
Use arrow functions only when you need to capture `this` from the enclosing scope.
Avoid syntactic sugar such as function expressions and method shorthand.

Good:

```js
function fetchUser(id) {
	return fetch("/users/" + id)
}
```

Good (arrow function to capture `this`):

```js
function Timer() {
	this.seconds = 0
	setInterval(() => {
		this.seconds++
	}, 1000)
}
```

Avoid (function expression):

```js
let fetchUser = function (id) { return fetch("/users/" + id) }
```

Avoid (method shorthand):

```js
let api = {
	fetchUser(id) { return fetch("/users/" + id) }
}
```

### Error Handling

Always handle errors explicitly. JS exceptions propagate silently up the call
stack, so unhandled failures cause the UI to freeze with no feedback.

#### New code

Use `try/catch` per async operation.
**Always check `response.ok`**: `fetch` does not throw on HTTP errors like 404 or 500.

```js
async function loadUser() {
	let response
	try {
		response = await fetch("/api/user")
	} catch (err) {
		showError("Network error: " + err.message)
		return
	}
	if (!response.ok) {
		showError("Server error: " + response.status)
		return
	}
	let data = await response.json()
	renderUser(data)
}
```

#### Retrofitting existing code

If a bare `fetch` call has no error handling at all,
appending `.catch` is the minimal change that prevents silent failures.
Prefer this over restructuring the whole function when the change is isolated.

Before:

```js
fetch("/api/user").then(function (r) { renderUser(r) })
```

After:

```js
fetch("/api/user")
	.then(function (r) { renderUser(r) })
	.catch(function (err) { showError(err.message) })
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
