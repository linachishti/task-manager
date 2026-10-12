"""In-memory user repository."""

DEFAULT_NOTIFICATION_PREFERENCE = "none"

_USERS = {
    1: {
        "id": 1,
        "name": "Lina",
        "notification_pref": DEFAULT_NOTIFICATION_PREFERENCE,
    },
    2: {
        "id": 2,
        "name": "Sam",
        "notification_pref": DEFAULT_NOTIFICATION_PREFERENCE,
    },
}


def get_user_by_id(user_id: int) -> dict | None:
    """Return a user by ID, or None if the user does not exist."""
    return _USERS.get(user_id)


def get_all_users() -> list[dict]:
    """Return all stored users."""
    return list(_USERS.values())


def get_user_notification_preference(user_id: int) -> str | None:
    """Return the notification preference of a stored user.

    Args:
        user_id: ID of the user whose preference to retrieve.

    Returns:
        The user's notification preference, or None if the user does not exist.
    """
    user = _USERS.get(user_id)
    if user is None:
        return None
    return user.get("notification_pref", DEFAULT_NOTIFICATION_PREFERENCE)


def update_user_notification_preference_record(
    user_id: int, preference: str
) -> dict | None:
    """Update the notification preference of a stored user.

    The preference is stored as given. Validation belongs in the service layer.

    Args:
        user_id: ID of the user to update.
        preference: New notification preference of the user.

    Returns:
        The updated user, or None if the user does not exist.
    """
    user = _USERS.get(user_id)
    if user is None:
        return None
    user["notification_pref"] = preference
    return user
