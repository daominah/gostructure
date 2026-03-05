# code-and-pr-review skill — WIP notes

## Done
- Created skill with 5 sections in priority order
- Section 1 "Code Meets Business Need": business intent source (ticket/Slack/spec), consistency check, clarity before coding
- Section 2 "Building It the Right Way": small PRs, no regressions, separate improvement commits
- Section 3 "Code Works as Expected": tests required, GIVEN/WHEN/THEN format
- Section 4 "End-User Verifiability": observable output for users to confirm
- Section 5 "Logging and Monitoring for Long-Running Features": log start/end, counts, errors

## Source material
- Key framework:
  1. Build the right thing (code meets business need)
  2. Build it the right way (small PRs, no regressions)
  3. Code works as expected (tests)
  4. Improve codebase continuously
  5. Share knowledge
- Iterative process: assigned → define PR → check DoR → plan & implement → review DoD → approve → deploy
- Anti-pattern to avoid: ticket → coding → review → definition unclear → major rework
- Roles: author (owns the change), reviewer (reviews, involved early), approver (owns the code)
- Guidelines: small PRs, short feedback loops, keep open PRs small

## Still to review
- Section titles 2-5: user approved "Code Meets Business Need" for section 1, other titles haven't been revisited yet
- May want to refine further based on user feedback
