"""User route-style functions.

These functions are intentionally simple so the architecture is easy to see.
"""

from services.users import (
    get_notification_preference,
    get_users,
    update_notification_preference,
)


def get_user_notifications(user_id: int) -> str:
    """Return a user's notification preference through the service layer.

    Equivalent to GET /users/{id}/notifications.

    Args:
        user_id: ID of the user whose preference to retrieve.

    Returns:
        The user's notification preference: "email", "sms", or "none".

    Raises:
        NotFoundError: If the user does not exist.
    """
    return get_notification_preference(user_id)


def update_user_notifications(user_id: int, preference: str) -> dict:
    """Update a user's notification preference through the service layer.

    Equivalent to PATCH /users/{id}/notifications.

    Args:
        user_id: ID of the user to update.
        preference: New notification preference: "email", "sms", or "none".

    Returns:
        The updated user.

    Raises:
        ValidationError: If the preference is not "email", "sms", or "none".
        NotFoundError: If the user does not exist.
    """
    return update_notification_preference(user_id, preference)


def list_users() -> list[dict]:
    """Return all users through the service layer.

    Equivalent to GET /users.

    Returns:
        All users, each including notification_pref, or an empty list if
        there are none.
    """
    return get_users()
