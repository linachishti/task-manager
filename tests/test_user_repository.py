import pytest

from repositories.users import get_all_users

TEST_USERS = {
    1: {"id": 1, "name": "Lina", "notification_pref": "none"},
    2: {"id": 2, "name": "Sam", "notification_pref": "email"},
}


@pytest.fixture(autouse=True)
def isolated_users(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        "repositories.users._USERS",
        {user_id: dict(user) for user_id, user in TEST_USERS.items()},
    )


def test_get_all_users_returns_all_stored_users_in_id_order() -> None:
    users = get_all_users()
    assert [user["id"] for user in users] == [1, 2]
    assert [user["notification_pref"] for user in users] == ["none", "email"]


def test_get_all_users_returns_empty_list_when_no_users(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("repositories.users._USERS", {})
    assert get_all_users() == []
