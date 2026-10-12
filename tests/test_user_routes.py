import pytest

from routes.users import (
    get_user_notifications,
    list_users,
    update_user_notifications,
)
from utils.errors import NotFoundError, ValidationError

TEST_USERS = {
    1: {"id": 1, "name": "Lina", "notification_pref": "none"},
    2: {"id": 2, "name": "Sam", "notification_pref": "none"},
}


@pytest.fixture(autouse=True)
def isolated_users(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "repositories.users._USERS",
        {user_id: dict(user) for user_id, user in TEST_USERS.items()},
    )


def test_get_user_notifications_returns_default_none() -> None:
    assert get_user_notifications(1) == "none"


def test_get_user_notifications_raises_for_missing_user() -> None:
    with pytest.raises(NotFoundError):
        get_user_notifications(999)


@pytest.mark.parametrize("preference", ["email", "sms", "none"])
def test_update_user_notifications_returns_updated_user(preference: str) -> None:
    updated = update_user_notifications(2, preference)
    assert updated["id"] == 2
    assert updated["notification_pref"] == preference
    assert get_user_notifications(2) == preference


@pytest.mark.parametrize("preference", ["push", "", None, 1])
def test_update_user_notifications_rejects_invalid_preference(
    preference: object,
) -> None:
    with pytest.raises(ValidationError):
        update_user_notifications(1, preference)
    assert get_user_notifications(1) == "none"


def test_update_user_notifications_raises_for_missing_user() -> None:
    with pytest.raises(NotFoundError):
        update_user_notifications(999, "email")


def test_update_user_notifications_validates_before_user_exists() -> None:
    with pytest.raises(ValidationError):
        update_user_notifications(999, "push")


def test_list_users_includes_notification_pref_for_every_user() -> None:
    users = list_users()
    assert [user["id"] for user in users] == [1, 2]
    assert all(user["notification_pref"] == "none" for user in users)


def test_list_users_returns_empty_list_when_no_users(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("repositories.users._USERS", {})
    assert list_users() == []


def test_list_users_reflects_patched_preference() -> None:
    update_user_notifications(1, "email")
    users = list_users()
    assert [user["notification_pref"] for user in users] == ["email", "none"]
