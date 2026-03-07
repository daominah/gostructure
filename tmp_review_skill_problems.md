# Vague Instructions in review-code-and-pr Skill

Good agent skill instructions are actionable, specific, and checkable.
Vague instructions lead to inconsistent behavior
because the AI has no criteria to decide what to flag.

## Broken instruction

Line 30-31: "The PR must link to its ticket ... if not linked:"
ends with a colon but has no follow-up action.
The AI does not know what to do when the link is missing.

## Subjective adjectives without criteria

Line 33: "Verify the sources ... are clear."
What makes a source clear vs unclear? No criteria given.
Concrete alternative: the ticket states expected behavior,
current behavior, and affected users.

Line 68: "Review risks from user inputs: is validation sufficient?"
Sufficient against what? No threat model or checklist provided.
Concrete alternative: check that user inputs are validated for type,
length, and format before use in queries, file paths, or shell commands.

Line 73: "Code should be easy to read, change, and debug
by someone who didn't write it."
This is a platitude. Every style guide says this.
Concrete alternative: flag functions longer than 50 lines,
more than 3 levels of nesting, or names that do not describe behavior.

## Unbounded scope

Line 51: "Check for changes that could break untested code paths."
Every codebase has untested paths. How far should the reviewer look?
Concrete alternative: check callers of modified functions
and shared state for side effects.

Line 53: "unnecessary load on shared resources."
Every query adds load. What threshold matters?
Concrete alternative: flag queries without WHERE clauses on large tables,
N+1 patterns, or loops that make network calls.

Line 74: "Improve the codebase where you touch it."
Unbounded. An AI following this literally could suggest refactors
on every review.
Concrete alternative: fix obvious issues (typos, dead code)
in lines you already modify.

## Missing thresholds

Line 61-62: "Long-running functions or background jobs
provide a way to inspect progress."
When does a function qualify as long-running? 1 second? 1 minute?
Concrete alternative: functions expected to run longer than 30 seconds
should expose progress.

Line 63: "Support for cancellation is a nice to have."
"Nice to have" gives the AI no decision criteria.
It will be consistently ignored.
Either remove it or make it conditional,
e.g., flag missing cancellation for operations that exceed 5 minutes.

## Human-oriented advice given to AI

Line 76: "Label nitpicks clearly
so the author knows what is blocking vs optional."
The Output Format section already separates blockers from nitpicks,
making this instruction redundant.
Either remove it or reword as:
"Classify each finding as blocker, suggestion, or nitpick
according to the Output Format."

## Not an action item

Line 87: "This prevents misalignment earlier in future work."
This is a rationale for lines 85-86, not a checklist item.
Move it above the list as context or remove it.
