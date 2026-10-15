# CLAUDE.md

## Commands
- Install dependencies with `python -m pip install -r requirements.txt`.
- Run tests with `.venv/bin/python3 -m pytest -q`.
- Run lint with `.venv/bin/python3 -m ruff check .`.
- Before finishing any code task, run `.venv/bin/python3 -m pytest -q` and fix any failures caused by the changes.
- In this project, use the virtual environment: run tests with `.venv/bin/python3 -m pytest -q` and lint with `.venv/bin/python3 -m ruff check .` (system `python3` does not have pytest installed).
- `/audit-errors <service file>` — checks service error handling and skips functions already using `AppError` correctly.
- `/scaffold-endpoint <resource> <METHOD>` — creates an API endpoint following the route, service, and schema patterns.
- `/verify-feature <feature>` — runs relevant tests, the complete pytest suite, and Ruff.

## Architecture
- Keep the project structure as `routes -> services -> repositories`.
- Routes should handle requests and responses, services should contain the main logic, and repositories should handle data access.
- Use `services/users.py` as the example to follow for service-layer code.
- Follow the existing style in `services/tasks.py` when changing or adding task functions.
- Do not call repository logic directly from a route if the project already expects that logic to go through a service.
- `routes/users.py` should only call functions in `services/users.py`, where notification preference validation and business logic happen, following the existing pattern in `services/users.py`.

## Conventions
- Use type hints for all new or modified functions.
- Use Google-style docstrings for all new or modified functions.
- Match the style in `services/users.py` when writing service functions.
- Use the `AppError` subclasses from `utils/errors.py` instead of plain built-in exceptions when a project-specific error fits.
- Keep existing function signatures unless the task specifically requires a change.
- Keep changes focused on the task instead of rewriting unrelated code.
- Add or update tests when service behavior changes.
- For refactors that do not change behavior, keep the existing tests and avoid adding unnecessary new tests.

## Do not touch
- Do not break the `routes -> services -> repositories` structure.
- Do not move service logic into route files.
- Do not rename or remove existing public service functions unless the task asks for it.
- Do not edit unrelated files just for cleanup.
- Do not import from `repositories/users.py` in `routes/users.py` or any other route file; routes must go through `services/users.py`.
- Do not validate notification preferences (`email`, `sms`, `none`) in `routes/users.py`; validation belongs in `services/users.py`.
- Do not return HTTP responses or put route-style logic in `services/users.py`; services return data or raise `AppError` subclasses from `utils/errors.py`.
- Do not add validation or business rules to `repositories/users.py`; it only stores and retrieves user data, and the stored field must be named `notification_pref`.

## Hooks
`.claude/hooks/guard_writes.py` is a PreToolUse hook that checks each tool call before it runs and blocks it with exit code 2 and an explanatory stderr message when a rule is violated. It blocks Write, Edit, and MultiEdit calls to `utils/errors.py` (matched case-insensitively, with `./`, `../`, and symlinks resolved), blocks `postgresql://` or `sqlite:///` connection strings written into `services/tasks.py` (use environment variables instead), and blocks Bash commands containing `DROP TABLE`/`TRUNCATE TABLE`, `rm -rf`, `git push --force`/`-f`, or indirect writes to `utils/errors.py` through `sed -i`, output redirection, `tee`, `cp`, `mv`, `dd`, or `truncate`, while read-only commands such as `cat utils/errors.py` are allowed. It is registered in `.claude/settings.json` under `hooks.PreToolUse` with the matcher `Write|Edit|MultiEdit|Bash` and runs `python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/guard_writes.py"`. To add a rule, add a path to `PROTECTED_FILES` or `CONNECTION_STRING_FILES`, or write a check that calls `block()` from `check_file_tool()` or `check_bash()`, then test it by piping simulated JSON tool inputs to the script and confirming exit code 2 for blocked cases and 0 for allowed ones.
