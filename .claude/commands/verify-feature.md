# Use this command after implementing a feature to check its tests and lint results. Do not use it to modify code.

## Goal
Verify the feature specified in $ARGUMENTS by running its relevant tests and the full project test suite.

## Context
Follow the testing patterns in tests/test_tasks.py, tests/test_users.py, and tests/test_tag_routes.py. Use the virtual environment commands documented in CLAUDE.md.

## Constraints
- Do not modify production files in repositories/, services/, routes/, schemas/, or app.py.
- Do not change tests just to make failures disappear.
- Do not modify utils/errors.py or requirements.txt.
- Report all test failures and warnings accurately.

## Verification
1. Find and run tests related to $ARGUMENTS.
2. Run .venv/bin/python3 -m pytest -q.
3. Run .venv/bin/python3 -m ruff check .
4. Report the exact number of passed and failed tests, warnings, and lint errors.
5. Summarize whether the feature passed the checks.
