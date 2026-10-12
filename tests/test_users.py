import pytest

from repositories.users import DEFAULT_NOTIFICATION_PREFERENCE
from services.users import (
    get_notification_preference,
    get_user,
    get_users,
    update_notification_preference,
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


def test_get_user_returns_existing_user() -> None:
    user = get_user(1)
    assert user["id"] == 1
    assert user["name"] == "Lina"


def test_get_user_raises_for_missing_user() -> None:
    with pytest.raises(NotFoundError):
        get_user(999)


def test_get_user_includes_notification_pref() -> None:
    user = get_user(1)
    assert user["notification_pref"] == "none"


def test_stored_users_all_include_notification_pref() -> None:
    from repositories import users as users_repository

    for user in users_repository._USERS.values():
        assert "notification_pref" in user


def test_default_notification_preference_is_none() -> None:
    assert DEFAULT_NOTIFICATION_PREFERENCE == "none"


@pytest.mark.parametrize("user_id", [1, 2])
def test_existing_users_default_to_none(user_id: int) -> None:
    assert get_notification_preference(user_id) == "none"


def test_get_notification_preference_raises_for_missing_user() -> None:
    with pytest.raises(NotFoundError):
        get_notification_preference(999)


@pytest.mark.parametrize("preference", ["email", "sms", "none"])
def test_update_notification_preference_saves_valid_preference(
    preference: str,
) -> None:
    updated = update_notification_preference(1, preference)
    assert updated["notification_pref"] == preference
    assert get_notification_preference(1) == preference
    assert get_user(1)["notification_pref"] == preference


@pytest.mark.parametrize("preference", ["push", "", None, 1])
def test_update_notification_preference_rejects_invalid_preference(
    preference: object,
) -> None:
    with pytest.raises(ValidationError):
        update_notification_preference(1, preference)
    assert get_notification_preference(1) == "none"


def test_update_notification_preference_raises_for_missing_user() -> None:
    with pytest.raises(NotFoundError):
        update_notification_preference(999, "email")


def test_update_notification_preference_validates_before_user_exists() -> None:
    with pytest.raises(ValidationError):
        update_notification_preference(999, "push")


def test_update_notification_preference_does_not_change_other_users() -> None:
    update_notification_preference(1, "sms")
    assert get_notification_preference(1) == "sms"
    assert get_notification_preference(2) == "none"


def test_get_users_returns_all_users_in_id_order() -> None:
    users = get_users()
    assert [user["id"] for user in users] == [1, 2]
    assert [user["name"] for user in users] == ["Lina", "Sam"]


def test_get_users_includes_notification_pref_for_every_user() -> None:
    users = get_users()
    assert all(user["notification_pref"] == "none" for user in users)


def test_get_users_returns_empty_list_when_no_users(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("repositories.users._USERS", {})
    assert get_users() == []


def test_get_users_reflects_updated_preference() -> None:
    update_notification_preference(2, "sms")
    users = get_users()
    assert [user["notification_pref"] for user in users] == ["none", "sms"]


def test_get_users_defaults_missing_notification_pref_to_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("repositories.users._USERS", {3: {"id": 3, "name": "Ana"}})
    assert get_users() == [{"id": 3, "name": "Ana", "notification_pref": "none"}]


def test_get_users_returns_copies_of_stored_users() -> None:
    users = get_users()
    users[0]["notification_pref"] = "push"
    users[0]["name"] = "Changed"
    assert get_notification_preference(1) == "none"
    assert get_user(1)["name"] == "Lina"
