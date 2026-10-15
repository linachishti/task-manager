# PA 6 — Retrospective

## 1. Slash Command Value

The slash command that saved me the most time was `/verify-feature`. In the third row of `COMMAND_LOG.md`, I used `/verify-feature tags` to check the tag feature. Instead of writing out a long prompt every time, I could use one command to run the relevant tests, the full test suite, and Ruff. Without the command, I would have had to explain all those steps separately. After fixing the empty command file, Claude ran 15 tag tests and all 114 project tests without changing any code. There was one warning, but all the tests passed.

## 2. Hook Reliability

The two bypass tests showed me that just having a hook doesn't mean every rule is being enforced correctly. In Vector 1 of `HOOK_LOG.md`, the hook allowed `Utils/Errors.py` because it was checking file paths with case-sensitive matching. I fixed this using `os.path.realpath` and `.casefold()`. In Vector 2, a Bash command using `sed -i` could get past the hook because it wasn't checking indirect file changes. After adding checks for those commands, all 83 simulated hook tests passed. This taught me that hooks need to be tested instead of just assuming they work.

## 3. Advisory vs. Deterministic Rules

One rule I would keep in `CLAUDE.md` is that new functions should have type hints and Google-style docstrings. I think this is better as a guideline for now because it focuses on code quality rather than preventing dangerous actions. I would enforce it automatically if the project started requiring every new public service function to pass documentation and type-hint checks before code could be merged. In that case, using a linter or CI check would make more sense.

## 4. Limits of Hooks

One thing I wanted to enforce was making sure every change to the service layer had a test covering it. A PreToolUse hook isn't the best way to do this because it only checks individual actions before they happen. It can't reliably tell whether the entire feature has enough tests. For example, when `/audit-errors services/tasks.py` fixed the title validation issue, the existing 99 tests passed, but no new test was added for that specific problem. A better solution would be to check test coverage during CI or use a final verification step before accepting the changes.