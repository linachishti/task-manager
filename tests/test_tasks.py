import pytest

from services.tasks import (
    create_task,
    filter_tasks_by_priority,
    get_task,
    get_tasks_for_user,
    update_task_priority,
)
from utils.errors import NotFoundError, ValidationError

FILTER_TASKS = {
    1: {"id": 1, "title": "Low", "user_id": 1, "priority": 1},
    2: {"id": 2, "title": "Medium A", "user_id": 1, "priority": 3},
    3: {"id": 3, "title": "Medium B", "user_id": 2, "priority": 3},
    4: {"id": 4, "title": "High", "user_id": 2, "priority": 5},
}


@pytest.fixture
def filter_tasks(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "repositories.tasks._TASKS",
        {task_id: dict(task) for task_id, task in FILTER_TASKS.items()},
    )


def test_get_task_returns_existing_task() -> None:
    task = get_task(1)
    assert task["id"] == 1


def test_get_tasks_for_user_returns_only_that_users_tasks() -> None:
    tasks = get_tasks_for_user(2)
    assert [task["id"] for task in tasks] == [3]


def test_get_tasks_for_user_returns_empty_list_when_user_has_no_tasks() -> None:
    assert get_tasks_for_user(999) == []


def test_create_task_returns_new_task() -> None:
    task = create_task("Read chapter", 1)
    assert task["title"] == "Read chapter"
    assert task["user_id"] == 1


def test_create_task_rejects_blank_title() -> None:
    with pytest.raises(ValidationError):
        create_task("   ", 1)


def test_create_task_defaults_priority_to_3() -> None:
    task = create_task("Review notes", 1)
    assert task["priority"] == 3


@pytest.mark.parametrize("priority", [1, 3, 5])
def test_create_task_stores_valid_priority(priority: int) -> None:
    task = create_task("Prioritized task", 1, priority)
    assert task["priority"] == priority
    assert get_task(task["id"])["priority"] == priority


@pytest.mark.parametrize("priority", [0, 6, -1, "3", 3.0, True, False, None])
def test_create_task_rejects_invalid_priority(priority: object) -> None:
    with pytest.raises(ValidationError):
        create_task("Invalid priority task", 1, priority)


def test_create_task_with_invalid_priority_does_not_store_task() -> None:
    count_before = len(get_tasks_for_user(1))
    with pytest.raises(ValidationError):
        create_task("Should not be stored", 1, 0)
    assert len(get_tasks_for_user(1)) == count_before


@pytest.mark.parametrize("priority", [1, 5])
def test_update_task_priority_changes_priority(priority: int) -> None:
    task = create_task("Task to update", 1)
    updated = update_task_priority(task["id"], priority)
    assert updated["priority"] == priority
    assert get_task(task["id"])["priority"] == priority


def test_update_task_priority_raises_for_missing_task() -> None:
    with pytest.raises(NotFoundError):
        update_task_priority(999, 4)


@pytest.mark.parametrize("priority", [0, 6, -1, "3", 3.0, True, False, None])
def test_update_task_priority_rejects_invalid_priority(priority: object) -> None:
    task = create_task("Task with invalid update", 1, 2)
    with pytest.raises(ValidationError):
        update_task_priority(task["id"], priority)
    assert get_task(task["id"])["priority"] == 2


def test_update_task_priority_validates_priority_before_task_exists() -> None:
    with pytest.raises(ValidationError):
        update_task_priority(999, 0)


def test_update_task_priority_does_not_change_other_tasks() -> None:
    task = create_task("Task to update", 1, 2)
    other_task = create_task("Other task", 1, 4)
    update_task_priority(task["id"], 5)
    assert get_task(task["id"])["priority"] == 5
    assert get_task(other_task["id"])["priority"] == 4


def test_filter_tasks_by_priority_returns_matching_tasks(filter_tasks: None) -> None:
    tasks = filter_tasks_by_priority(3)
    assert [task["id"] for task in tasks] == [2, 3]
    assert all(task["priority"] == 3 for task in tasks)


def test_filter_tasks_by_priority_returns_empty_list_when_none_match(
    filter_tasks: None,
) -> None:
    assert filter_tasks_by_priority(2) == []


@pytest.mark.parametrize("priority", [0, 6, -1, "3", 3.0, True, False, None])
def test_filter_tasks_by_priority_rejects_invalid_priority(
    filter_tasks: None, priority: object
) -> None:
    with pytest.raises(ValidationError):
        filter_tasks_by_priority(priority)
