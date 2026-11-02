"""Minimal item service with a real SQLite repository and injectable notifier."""


class SQLiteItemRepository:
    def __init__(self, connection):
        self.connection = connection
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS items ("
            "id INTEGER PRIMARY KEY, name TEXT NOT NULL)"
        )

    def save(self, name):
        cursor = self.connection.execute(
            "INSERT INTO items (name) VALUES (?)", (name,)
        )
        self.connection.commit()
        return cursor.lastrowid

    def find(self, item_id):
        row = self.connection.execute(
            "SELECT id, name FROM items WHERE id = ?", (item_id,)
        ).fetchone()
        return {"id": row[0], "name": row[1]} if row else None


class ItemService:
    def __init__(self, repository, notifier):
        self.repository = repository
        self.notifier = notifier

    def create_item(self, name):
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Item name must not be empty")
        item_id = self.repository.save(clean_name)
        self.notifier.item_created(item_id, clean_name)
        return {"id": item_id, "name": clean_name}

    def get_item(self, item_id):
        return self.repository.find(item_id)
