#!/usr/bin/env python3
"""PreToolUse guard for the task-manager project.

Blocks direct and Bash-based writes to utils/errors.py, destructive Bash
commands, and database connection strings written into services/tasks.py.
Exits with code 2 to block a tool call; the stderr message is shown to Claude.
"""

import json
import os
import re
import shlex
import sys

PROTECTED_FILES = ("utils/errors.py",)
CONNECTION_STRING_FILES = ("services/tasks.py",)

SQL_PATTERN = re.compile(r"\b(DROP|TRUNCATE)\s+TABLE\b", re.IGNORECASE)
CONNECTION_STRING_PATTERN = re.compile(
    r"\b(postgresql://|sqlite:///)", re.IGNORECASE
)
SEGMENT_SPLIT = re.compile(r"&&|\|\||[;|\n]")

# Shell redirection operators whose next word is a file being written.
REDIRECT_OPERATORS = (">", ">>", ">|", "&>", "&>>", "<>")
# Words that run another command; the real command name follows them.
COMMAND_WRAPPERS = ("sudo", "env", "command", "nohup", "time", "xargs")
# Commands that write to (or delete) any file argument they are given.
WRITES_ANY_ARGUMENT = ("tee", "mv", "rm", "unlink", "truncate", "shred")
# Commands that write only to their last (destination) argument.
WRITES_LAST_ARGUMENT = ("cp", "install", "rsync", "ln")
# Commands that write their file arguments only with an in-place flag.
WRITES_IN_PLACE = ("sed", "gsed", "perl")


def block(message: str) -> None:
    """Print a block message to stderr and exit with code 2.

    Args:
        message: Reason the tool call was blocked.
    """
    print(f"BLOCKED by guard_writes.py: {message}", file=sys.stderr)
    sys.exit(2)


def project_dir() -> str:
    """Return the resolved project root directory.

    Returns:
        The real path of CLAUDE_PROJECT_DIR, or of the current directory.
    """
    return os.path.realpath(os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()))


def project_relative(file_path: str) -> str:
    """Return a file path relative to the project root, for messages.

    Args:
        file_path: Absolute or project-relative path from the tool input.

    Returns:
        The normalized path relative to the project root.
    """
    root = project_dir()
    return os.path.relpath(os.path.realpath(os.path.join(root, file_path)), root)


def matches_path(file_path: str, paths: tuple[str, ...], base_dir: str) -> bool:
    """Return True if a path refers to one of the given files, ignoring case.

    Both paths are resolved with realpath (absolute, ./ and ../ folded,
    symlinks followed) and compared with casefold, because the default
    macOS filesystem treats Utils/Errors.py and utils/errors.py as the
    same file.

    Args:
        file_path: Absolute or relative path to check.
        paths: Project-relative paths to match against.
        base_dir: Directory that a relative file_path is resolved against.

    Returns:
        Whether file_path matches an entry in paths.
    """
    if not file_path:
        return False
    root = project_dir()
    target = os.path.realpath(os.path.join(base_dir, file_path)).casefold()
    return any(
        target == os.path.join(root, path).casefold() for path in paths
    )


def is_protected(file_path: str, base_dir: str | None = None) -> bool:
    """Return True if a path refers to a protected file, ignoring case.

    Args:
        file_path: Absolute or relative path to check.
        base_dir: Directory that a relative path is resolved against.
            Defaults to the project root.

    Returns:
        Whether the path matches an entry in PROTECTED_FILES.
    """
    return matches_path(file_path, PROTECTED_FILES, base_dir or project_dir())


def written_content(tool_name: str, tool_input: dict) -> str:
    """Return all text a Write, Edit, or MultiEdit call would write.

    Args:
        tool_name: Name of the tool being called.
        tool_input: The tool's input parameters.

    Returns:
        The text the call would write, or an empty string.
    """
    if tool_name == "Write":
        return tool_input.get("content", "")
    if tool_name == "Edit":
        return tool_input.get("new_string", "")
    if tool_name == "MultiEdit":
        return "\n".join(
            edit.get("new_string", "") for edit in tool_input.get("edits", [])
        )
    return ""


def check_file_tool(tool_name: str, tool_input: dict) -> None:
    """Apply the protected-file and connection-string guards.

    Args:
        tool_name: Name of the tool being called.
        tool_input: The tool's input parameters.
    """
    file_path = tool_input.get("file_path", "")
    relative = project_relative(file_path)
    if is_protected(file_path):
        block(
            f"{relative} is protected (paths are matched ignoring case). "
            "Do not modify the shared AppError hierarchy; add handling in "
            "the service layer instead."
        )
    if matches_path(file_path, CONNECTION_STRING_FILES, project_dir()):
        match = CONNECTION_STRING_PATTERN.search(
            written_content(tool_name, tool_input)
        )
        if match:
            block(
                f"Refusing to write a '{match.group(1)}' connection string "
                f"into {relative}. Credentials and connection strings must "
                "come from environment variables (e.g. "
                "os.environ['DATABASE_URL']), not source code, so they are "
                "never committed to git."
            )


def tokens(segment: str) -> list[str]:
    """Split one command segment into shell words and operators.

    Redirection operators such as > and >> become separate tokens even
    when written without spaces (echo x>file).

    Args:
        segment: A single command without ;, &&, ||, or | separators.

    Returns:
        The shell tokens, or whitespace-split words if quoting is unbalanced.
    """
    lexer = shlex.shlex(segment, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    try:
        return list(lexer)
    except ValueError:
        return segment.split()


def is_rm_rf(words: list[str]) -> bool:
    """Return True if the words contain rm with recursive and force flags.

    Args:
        words: Shell words of one command segment.

    Returns:
        Whether the segment is an rm call with both -r and -f behavior.
    """
    for i, word in enumerate(words):
        if os.path.basename(word) != "rm":
            continue
        recursive = force = False
        for flag in words[i + 1:]:
            if not flag.startswith("-"):
                continue
            if flag == "--recursive":
                recursive = True
            elif flag == "--force":
                force = True
            elif not flag.startswith("--"):
                recursive |= "r" in flag or "R" in flag
                force |= "f" in flag
        if recursive and force:
            return True
    return False


def is_force_push(words: list[str]) -> bool:
    """Return True if the words are a git push with --force or -f.

    Args:
        words: Shell words of one command segment.

    Returns:
        Whether the segment force-pushes with git.
    """
    if "git" not in words or "push" not in words:
        return False
    return words.index("push") > words.index("git") and (
        "--force" in words or "-f" in words
    )


def command_and_args(words: list[str]) -> tuple[str, list[str]]:
    """Return the command name and its arguments, skipping wrappers.

    Leading VAR=value assignments and wrappers such as sudo or xargs are
    skipped so that "sudo sed -i ..." is treated as a sed command.

    Args:
        words: Shell words of one command segment.

    Returns:
        The command's basename and the words after it.
    """
    for i, word in enumerate(words):
        name = os.path.basename(word)
        if name in COMMAND_WRAPPERS or ("=" in word and not word.startswith("-")):
            continue
        if word.startswith("-") and i > 0:
            continue
        return name, words[i + 1:]
    return "", []


def has_in_place_flag(args: list[str]) -> bool:
    """Return True if the arguments include an in-place edit flag.

    Matches -i, -i.bak, combined short flags such as -pi or -Ei, and
    --in-place.

    Args:
        args: Arguments that follow sed or perl.

    Returns:
        Whether the command edits files in place.
    """
    return any(
        arg.startswith("--in-place")
        or (arg.startswith("-") and not arg.startswith("--") and "i" in arg)
        for arg in args
    )


def protected_write_target(words: list[str], base_dir: str) -> str | None:
    """Return how a command segment writes to a protected file, if it does.

    Args:
        words: Shell tokens of one command segment.
        base_dir: Directory that relative paths are resolved against.

    Returns:
        A short description of the write (for example "sed -i" or
        "output redirection"), or None if no protected file is written.
    """
    for operator, target in zip(words, words[1:]):
        if operator in REDIRECT_OPERATORS and is_protected(target, base_dir):
            return "output redirection"
    name, args = command_and_args(words)
    positional = [arg for arg in args if not arg.startswith("-")]
    if name in WRITES_ANY_ARGUMENT:
        if any(is_protected(arg, base_dir) for arg in positional):
            return name
    elif name in WRITES_LAST_ARGUMENT:
        if "-t" in args or "--target-directory" in args:
            return None
        if positional and is_protected(positional[-1], base_dir):
            return name
    elif name in WRITES_IN_PLACE and has_in_place_flag(args):
        if any(is_protected(arg, base_dir) for arg in positional):
            return f"{name} -i"
    elif name == "dd":
        targets = [arg[3:] for arg in args if arg.startswith("of=")]
        if any(is_protected(target, base_dir) for target in targets):
            return "dd of="
    return None


def check_bash(command: str, cwd: str) -> None:
    """Apply the destructive-command and protected-file guards to Bash.

    Args:
        command: The full Bash command string.
        cwd: Working directory the command runs in.
    """
    if SQL_PATTERN.search(command):
        block("DROP TABLE / TRUNCATE TABLE is not allowed.")
    for segment in SEGMENT_SPLIT.split(command):
        words = tokens(segment)
        if is_rm_rf(words):
            block("rm -rf is not allowed. Delete specific files explicitly.")
        if is_force_push(words):
            block(
                "git push --force is not allowed; it can overwrite shared "
                "history."
            )
        method = protected_write_target(words, cwd)
        if method:
            block(
                f"Bash command writes to a protected file via {method}: "
                f"{segment.strip()!r}. utils/errors.py is protected (paths "
                "are matched ignoring case); reading it with cat, grep, or "
                "similar is allowed, but it must not be modified."
            )


def main() -> None:
    """Read the hook payload from stdin and apply the matching guard."""
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        block("could not parse hook input.")
    tool_name = payload.get("tool_name", "")
    tool_input = payload.get("tool_input", {})
    if tool_name in ("Write", "Edit", "MultiEdit"):
        check_file_tool(tool_name, tool_input)
    elif tool_name == "Bash":
        cwd = payload.get("cwd") or project_dir()
        check_bash(tool_input.get("command", ""), cwd)
    sys.exit(0)


if __name__ == "__main__":
    main()
