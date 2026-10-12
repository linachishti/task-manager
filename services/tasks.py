"""Task service functions."""

from repositories.tasks import (
    DEFAULT_PRIORITY,
    create_task_record,
    get_all_tasks,
    get_task_by_id,
    get_tasks_by_priority,
    update_task_priority_record,
)
from utils.errors import NotFoundError, ValidationError

MIN_PRIORITY = 1
MAX_PRIORITY = 5


def get_task(task_id: int) -> dict:
    """Get a task by ID.

    Args:
        task_id: ID of the task to retrieve.

    Returns:
        The matching task.

    Raises:
        NotFoundError: If the task does not exist.
    """
    task = get_task_by_id(task_id)
    if task is None:
        raise NotFoundError(f"Task {task_id} was not found.")
    return task


def get_tasks_for_user(user_id: int) -> list[dict]:
    """Get all tasks for a user.

    Args:
        user_id: ID of the user whose tasks to retrieve.

    Returns:
        The user's tasks, or an empty list if they have none.
    """
    tasks = [task for task in get_all_tasks() if task["user_id"] == user_id]
    return tasks


def _validate_priority(priority: int) -> None:
    """Check that a task priority is an integer from 1 to 5.

    Args:
        priority: Priority value to check.

    Raises:
        ValidationError: If the priority is not an int, is a bool, or is
            outside the range MIN_PRIORITY to MAX_PRIORITY.
    """
    if (
        isinstance(priority, bool)
        or not isinstance(priority, int)
        or not MIN_PRIORITY <= priority <= MAX_PRIORITY
    ):
        raise ValidationError("Task priority must be an integer from 1 to 5.")


def create_task(title: str, user_id: int, priority: int = DEFAULT_PRIORITY) -> dict:
    """Create a new task.

    Args:
        title: Title of the task to create.
        user_id: ID of the user who owns the task.
        priority: Priority of the task, from 1 to 5. Defaults to DEFAULT_PRIORITY.

    Returns:
        The newly created task.

    Raises:
        ValidationError: If the title is empty or only whitespace, or if the
            priority is not an integer from 1 to 5.
    """
    if not title.strip():
        raise ValidationError("Task title cannot be empty.")
    _validate_priority(priority)
    task = create_task_record(title, user_id, priority)
    return task


def update_task_priority(task_id: int, priority: int) -> dict:
    """Update the priority of an existing task.

    The priority is validated before the task is looked up, so an invalid
    priority raises ValidationError even when the task does not exist.

    Args:
        task_id: ID of the task to update.
        priority: New priority of the task, from 1 to 5.

    Returns:
        The updated task.

    Raises:
        ValidationError: If the priority is not an integer from 1 to 5.
        NotFoundError: If the task does not exist.
    """
    _validate_priority(priority)
    if get_task_by_id(task_id) is None:
        raise NotFoundError(f"Task {task_id} was not found.")
    task = update_task_priority_record(task_id, priority)
    return task


def filter_tasks_by_priority(priority: int) -> list[dict]:
    """Get all tasks with the given priority.

    Args:
        priority: Priority to filter by, from 1 to 5.

    Returns:
        The matching tasks, or an empty list if none match.

    Raises:
        ValidationError: If the priority is not an integer from 1 to 5.
    """
    _validate_priority(priority)
    tasks = get_tasks_by_priority(priority)
    return tasks
