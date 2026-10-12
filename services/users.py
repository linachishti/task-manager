"""User service functions."""

from repositories.users import (
    DEFAULT_NOTIFICATION_PREFERENCE,
    get_all_users,
    get_user_by_id,
    get_user_notification_preference,
    update_user_notification_preference_record,
)
from utils.errors import NotFoundError, ValidationError

VALID_NOTIFICATION_PREFERENCES = ("email", "sms", "none")


def get_user(user_id: int) -> dict:
    """Get a user by ID.

    Args:
        user_id: ID of the user to retrieve.

    Returns:
        The matching user.

    Raises:
        NotFoundError: If the user does not exist.
    """
    user = get_user_by_id(user_id)
    if user is None:
        raise NotFoundError(f"User {user_id} was not found.")
    return user


def _validate_notification_preference(preference: str) -> None:
    """Check that a notification preference is one of the valid options.

    Args:
        preference: Notification preference to check.

    Raises:
        ValidationError: If the preference is not a string or is not one of
            VALID_NOTIFICATION_PREFERENCES.
    """
    if (
        not isinstance(preference, str)
        or preference not in VALID_NOTIFICATION_PREFERENCES
    ):
        raise ValidationError(
            "Notification preference must be one of: email, sms, none."
        )


def get_notification_preference(user_id: int) -> str:
    """Get a user's notification preference.

    Args:
        user_id: ID of the user whose preference to retrieve.

    Returns:
        The user's notification preference: "email", "sms", or "none".

    Raises:
        NotFoundError: If the user does not exist.
    """
    preference = get_user_notification_preference(user_id)
    if preference is None:
        raise NotFoundError(f"User {user_id} was not found.")
    return preference


def update_notification_preference(user_id: int, preference: str) -> dict:
    """Update a user's notification preference.

    The preference is validated before the user is looked up, so
    ValidationError is raised first when both are invalid.

    Args:
        user_id: ID of the user to update.
        preference: New notification preference: "email", "sms", or "none".

    Returns:
        The updated user.

    Raises:
        ValidationError: If the preference is not "email", "sms", or "none".
        NotFoundError: If the user does not exist.
    """
    _validate_notification_preference(preference)
    user = update_user_notification_preference_record(user_id, preference)
    if user is None:
        raise NotFoundError(f"User {user_id} was not found.")
    return user


def get_users() -> list[dict]:
    """Get all users, each including a notification preference.

    Each user is returned as a copy, so changes to a returned dictionary do
    not affect stored user data. A stored user without a notification
    preference is returned with DEFAULT_NOTIFICATION_PREFERENCE.

    Returns:
        All users in ID order, or an empty list if there are none.
    """
    return [
        {
            **user,
            "notification_pref": user.get(
                "notification_pref", DEFAULT_NOTIFICATION_PREFERENCE
            ),
        }
        for user in get_all_users()
    ]
