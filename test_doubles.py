"""Unit tests illustrating five common test double types."""

from unittest.mock import Mock

from item_demo import ItemService


class FakeRepository:
    """FAKE: working in-memory replacement for a database-backed repository."""

    def __init__(self):
        self.items = {}
        self.next_id = 1

    def save(self, name):
        item_id = self.next_id
        self.next_id += 1
        self.items[item_id] = {"id": item_id, "name": name}
        return item_id

    def find(self, item_id):
        return self.items.get(item_id)


class StubRepository:
    """STUB: returns a predefined response regardless of the requested ID."""

    def find(self, item_id):
        return {"id": 42, "name": "preset"}


class SpyNotifier:
    """SPY: records interactions for assertions."""

    def __init__(self):
        self.calls = []

    def item_created(self, item_id, name):
        self.calls.append((item_id, name))


class DummyNotifier:
    """DUMMY: placeholder unused in read-only tests."""

    def item_created(self, item_id, name):
        raise AssertionError("Read-only test should never send notifications")


def test_fake_repository_and_spy_notifier():
    repository = FakeRepository()
    notifier = SpyNotifier()
    service = ItemService(repository, notifier)

    created = service.create_item("mouse")
    assert service.get_item(created["id"]) == {"id": 1, "name": "mouse"}
    assert notifier.calls == [(1, "mouse")]


def test_stub_returns_fixed_data():
    service = ItemService(StubRepository(), DummyNotifier())
    assert service.get_item(1000) == {"id": 42, "name": "preset"}


def test_dummy_is_not_used_for_read_only_operation():
    repository = FakeRepository()
    repository.save("monitor")
    service = ItemService(repository, DummyNotifier())
    assert service.get_item(1)["name"] == "monitor"


def test_mock_checks_expected_interactions():
    repository = FakeRepository()
    notifier = Mock()
    service = ItemService(repository, notifier)
    service.create_item("keyboard")
    notifier.item_created.assert_called_once_with(1, "keyboard")
