"""Integration tests: service + real (in-memory) SQLite database."""

import sqlite3
from unittest.mock import Mock

import pytest

from item_demo import ItemService, SQLiteItemRepository


def test_create_and_fetch_item():
    with sqlite3.connect(":memory:") as connection:
        repository = SQLiteItemRepository(connection)
        notifier = Mock()  # Mock the external notification dependency
        service = ItemService(repository, notifier)

        created = service.create_item(" keyboard ")
        assert created == {"id": 1, "name": "keyboard"}
        assert service.get_item(1) == created

        # Verify persistence independently of the repository API.
        row = connection.execute(
            "SELECT name FROM items WHERE id = ?", (1,)
        ).fetchone()
        assert row == ("keyboard",)
        notifier.item_created.assert_called_once_with(1, "keyboard")


def test_reject_empty_name_without_writing():
    with sqlite3.connect(":memory:") as connection:
        repository = SQLiteItemRepository(connection)
        notifier = Mock()
        service = ItemService(repository, notifier)

        with pytest.raises(ValueError, match="must not be empty"):
            service.create_item("   ")

        assert connection.execute("SELECT COUNT(*) FROM items").fetchone() == (0,)
        notifier.item_created.assert_not_called()
