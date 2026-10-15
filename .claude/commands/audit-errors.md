# Error-Handling Audit

## Goal
Audit the service file specified in `$ARGUMENTS` for incorrect error handling. Replace raw exceptions with the appropriate `AppError` subclasses when necessary.

## Context
Follow the error-handling conventions in `utils/errors.py` and the existing patterns in `services/users.py`.

## Constraints
- Only modify the service file specified in `$ARGUMENTS`.
- Do not modify `utils/errors.py`, `routes/tasks.py`, or `routes/users.py`.
- If a function already uses the correct `AppError` subclass, skip it. Do not rewrite working functions.
- Preserve existing behavior and function signatures unless fixing incorrect error handling requires a change.
- Do not change unrelated code.

## Verification

Audit one function at a time. Immediately after reviewing each function, run `.venv/bin/python3 -m pytest -q`, even if the function did not need any changes.

Do not wait until the entire audit is complete to run tests. Report the test result for each individual function.

After auditing all functions, run `.venv/bin/python3 -m ruff check .` and summarize any fixes.