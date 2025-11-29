#!/usr/bin/env python3
"""
Medium-complexity module for benchmarking
Expected LJPW: Balanced across dimensions
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class User:
    """User data model with validation"""

    id: int
    name: str
    email: str
    active: bool = True

    def __post_init__(self):
        """Validate user data"""
        if not self.name:
            raise ValueError("Name cannot be empty")
        if "@" not in self.email:
            raise ValueError("Invalid email format")
        if self.id < 0:
            raise ValueError("ID must be positive")


class UserRepository:
    """Repository for user management with error handling"""

    def __init__(self):
        self._users: Dict[int, User] = {}
        self._logger = logging.getLogger(__name__)

    def add_user(self, user: User) -> None:
        """
        Add a user to the repository.

        Args:
            user: User object to add

        Raises:
            ValueError: If user already exists
        """
        if user.id in self._users:
            self._logger.error(f"User {user.id} already exists")
            raise ValueError(f"User with ID {user.id} already exists")

        try:
            self._users[user.id] = user
            self._logger.info(f"Added user {user.id}")
        except Exception as e:
            self._logger.error(f"Failed to add user: {e}")
            raise

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            user_id: ID of user to retrieve

        Returns:
            User if found, None otherwise
        """
        if user_id < 0:
            self._logger.warning(f"Invalid user ID: {user_id}")
            return None

        return self._users.get(user_id)

    def get_active_users(self) -> List[User]:
        """
        Get all active users.

        Returns:
            List of active users
        """
        try:
            return [u for u in self._users.values() if u.active]
        except Exception as e:
            self._logger.error(f"Failed to get active users: {e}")
            return []

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id: ID of user to delete

        Returns:
            True if deleted, False if not found
        """
        if user_id in self._users:
            try:
                del self._users[user_id]
                self._logger.info(f"Deleted user {user_id}")
                return True
            except Exception as e:
                self._logger.error(f"Failed to delete user: {e}")
                return False
        return False


def validate_email(email: str) -> bool:
    """
    Validate email format.

    Args:
        email: Email address to validate

    Returns:
        True if valid format
    """
    if not email:
        return False

    return "@" in email and "." in email.split("@")[1]


def process_users(users: List[Dict[str, Any]]) -> List[User]:
    """
    Process raw user data into User objects.

    Args:
        users: List of user dictionaries

    Returns:
        List of validated User objects

    Raises:
        ValueError: If user data is invalid
    """
    if not users:
        raise ValueError("User list cannot be empty")

    result = []
    for user_data in users:
        try:
            user = User(
                id=user_data["id"],
                name=user_data["name"],
                email=user_data["email"],
                active=user_data.get("active", True),
            )
            result.append(user)
        except KeyError as e:
            logging.error(f"Missing required field: {e}")
            raise ValueError(f"Invalid user data: missing {e}")
        except Exception as e:
            logging.error(f"Failed to process user: {e}")
            raise

    return result
